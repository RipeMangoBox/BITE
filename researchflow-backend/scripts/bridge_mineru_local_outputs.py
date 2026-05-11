import asyncio
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from sqlalchemy import text

from backend.database import async_session
from backend.config import settings
from backend.services.object_storage import get_storage
from backend.services.vault_export_v6 import export_vault

ROOT = Path(__file__).resolve().parents[2]
MINERU_BASE = ROOT / '_private' / 'mineru_comparison' / 'outputs'

PAPERS = {
    'AIREAI': {
        'paper_id': '147942cd-6284-4aa7-bddf-a097b112e56f',
        'subdir': 'AIREAI',
        'docdir': 'A.I.R._Enabling_Adaptive_Iterative_and_Reasoning-based_Frame_Selection_For_Video__7f3042d38a50',
    },
    '3DGEER': {
        'paper_id': '08f8f231-d7ae-4127-a47d-a5ddb1fea800',
        'subdir': '3DGEER',
        'docdir': '3DGEER_3D_Gaussian_Rendering_Made_Exact_and_Efficient_for_Generic_Cameras__ICLR_2026_3dgeer_3d_gaussian_rendering_made_exact_and_efficient_for_generic_cameras',
    },
    'ADEPT': {
        'paper_id': '8582023f-c0db-48e3-8411-b2b4e1441acc',
        'subdir': 'ADEPT',
        'docdir': 'ADEPT_Continual_Pretraining_via_Adaptive_Expansion_and_Dynamic_Decoupled_Tuning__86dbc0c7fcb8',
    },
    'ACE': {
        'paper_id': 'a58dd10c-8e25-458e-b37c-1fb35a62eed3',
        'subdir': 'ACE',
        'docdir': 'ACE_Attribution-Controlled_Knowledge_Editing_for_Multi-hop_Factual_Recall__35b2e01b1246',
    },
    'AC-Sampler': {
        'paper_id': 'c28f1e8c-dcaf-437c-afb4-805e6f6d1803',
        'subdir': 'AC-Sampler',
        'docdir': 'AC-Sampler_Accelerate_and_Correct_Diffusion_Sampling_with_Metropolis-Hastings_Al__ce4567433865',
    },
}

CAPTION_RE = re.compile(r'^(Figure|Fig\.?|Table)\s*(\d+)', re.I)


def load_mineru_payload(cfg):
    base = MINERU_BASE / cfg['subdir'] / cfg['docdir'] / 'auto'
    md_path = next(base.glob('*.md'))
    json_path = next(base.glob('*content_list_v2.json'))
    md = md_path.read_text(errors='ignore')
    content = json.loads(json_path.read_text())
    return base, md, content


def extract_formulas(md: str):
    out = []
    for m in re.finditer(r'\$\$(.+?)\$\$', md, re.DOTALL):
        latex = m.group(1).strip()
        if latex:
            out.append(latex)
    dedup = []
    seen = set()
    for f in out:
        if f not in seen:
            seen.add(f)
            dedup.append(f)
    return dedup


def normalize_tables(content):
    tables = []
    for page in content:
        if not isinstance(page, list):
            continue
        for item in page:
            if not isinstance(item, dict) or item.get('type') != 'table':
                continue
            c = item.get('content') or {}
            captions = c.get('table_caption') or []
            cap_text = ' '.join(x.get('content','') for x in captions if isinstance(x, dict)).strip()
            m = CAPTION_RE.match(cap_text)
            table_num = int(m.group(2)) if m and m.group(1).lower().startswith('table') else None
            tables.append({
                'table_num': table_num,
                'caption': cap_text,
                'html': c.get('html',''),
                'csv': c.get('csv',''),
                'mineru_confidence': 1.0,
            })
    return tables


def normalize_figures(content):
    figs = []
    for page in content:
        if not isinstance(page, list):
            continue
        for item in page:
            if not isinstance(item, dict) or item.get('type') not in ('image','table','chart'):
                continue
            c = item.get('content') or {}
            src = (c.get('image_source') or {}).get('path')
            if not src:
                continue
            cap_key = 'table_caption' if item.get('type') == 'table' else 'image_caption'
            if item.get('type') == 'chart':
                cap_key = 'chart_caption'
            caps = c.get(cap_key) or []
            caption = ' '.join(x.get('content','') for x in caps if isinstance(x, dict)).strip()
            m = CAPTION_RE.match(caption)
            if m:
                label = f"{'Table' if m.group(1).lower().startswith('table') else 'Figure'} {m.group(2)}"
            else:
                label = None
            figs.append({
                'src_rel': src,
                'label': label,
                'type': 'table' if item.get('type') == 'table' else 'figure',
                'caption': caption,
                'bbox': item.get('bbox'),
            })
    dedup = []
    seen = set()
    for f in figs:
        key = (f['label'], f['src_rel'])
        if key in seen:
            continue
        seen.add(key)
        dedup.append(f)
    return dedup


async def bridge_one(session, storage, name, cfg):
    paper_id = cfg['paper_id']
    base, md, content = load_mineru_payload(cfg)
    formulas = extract_formulas(md)
    tables = normalize_tables(content)
    figures = normalize_figures(content)

    figure_records = []
    for idx, fig in enumerate(figures, start=1):
        if not fig['label']:
            continue
        src = base / fig['src_rel']
        if not src.exists():
            continue
        ext = src.suffix.lower() or '.png'
        object_key = f"papers/{paper_id}/figures/{fig['label'].replace(' ', '_')}{ext}"
        await storage.put(object_key, src.read_bytes())
        figure_records.append({
            'figure_num': idx,
            'label': fig['label'],
            'type': fig['type'],
            'semantic_role': 'other',
            'page_num': None,
            'bbox': fig.get('bbox'),
            'object_key': object_key,
            'public_url': storage.get_public_url(object_key),
            'caption': fig['caption'],
            'description': '',
            'width': None,
            'height': None,
            'size_bytes': src.stat().st_size,
            'extraction_method': 'mineru_cli_bridge',
        })

    row = (await session.execute(text('''
        SELECT id, evidence_spans
        FROM paper_analyses
        WHERE paper_id = :pid AND level = 'l2_parse' AND is_current = true
        LIMIT 1
    '''), {'pid': paper_id})).mappings().first()
    if not row:
        raise RuntimeError(f'No current L2 row for {name}')
    evidence = dict(row['evidence_spans'] or {})
    parse_meta = dict(evidence.get('parse_metadata') or {})
    parsers = list(parse_meta.get('parsers_used') or [])
    if 'mineru' not in parsers:
        parsers.append('mineru')
    parse_meta.update({
        'parsers_used': parsers,
        'mineru_available': True,
        'mineru_table_count': len(tables),
        'mineru_formula_count': len(formulas),
        'final_formula_count': len(formulas),
        'formula_source': 'mineru',
    })
    evidence['parse_metadata'] = parse_meta
    evidence['mineru_markdown'] = md[:10000]
    evidence['mineru_reading_order'] = []
    evidence['mineru_doc_metadata'] = {'bridge': 'local_mineru_cli'}

    await session.execute(text('''
        UPDATE paper_analyses
        SET extracted_formulas = :formulas,
            extracted_tables = CAST(:tables AS jsonb),
            extracted_figure_images = CAST(:figs AS jsonb),
            evidence_spans = CAST(:evidence AS jsonb)
        WHERE id = :id
    '''), {
        'id': str(row['id']),
        'formulas': formulas,
        'tables': json.dumps(tables, ensure_ascii=False),
        'figs': json.dumps(figure_records, ensure_ascii=False),
        'evidence': json.dumps(evidence, ensure_ascii=False),
    })

    await session.execute(text('DELETE FROM paper_figures WHERE paper_id = :pid'), {'pid': paper_id})
    for rec in figure_records:
        await session.execute(text('''
            INSERT INTO paper_figures (
                paper_id, label, type, semantic_role, page_num, bbox,
                object_key, public_url, caption, description,
                width, height, size_bytes, extraction_method
            ) VALUES (
                :paper_id, :label, :type, :semantic_role, :page_num, CAST(:bbox AS jsonb),
                :object_key, :public_url, :caption, :description,
                :width, :height, :size_bytes, :extraction_method
            )
        '''), {
            'paper_id': paper_id,
            'label': rec['label'],
            'type': rec['type'],
            'semantic_role': rec['semantic_role'],
            'page_num': rec['page_num'],
            'bbox': json.dumps(rec['bbox']) if rec['bbox'] is not None else None,
            'object_key': rec['object_key'],
            'public_url': rec['public_url'],
            'caption': rec['caption'],
            'description': rec['description'],
            'width': rec['width'],
            'height': rec['height'],
            'size_bytes': rec['size_bytes'],
            'extraction_method': rec['extraction_method'],
        })

    print(f'{name}: formulas={len(formulas)} tables={len(tables)} figs={len(figure_records)}')


async def main():
    storage = get_storage()
    async with async_session() as session:
        for name, cfg in PAPERS.items():
            await bridge_one(session, storage, name, cfg)
        await session.commit()
        result = await export_vault(session, vault_dir=settings.obsidian_vault_dir)
        print('export_result=', result)

if __name__ == '__main__':
    asyncio.run(main())
