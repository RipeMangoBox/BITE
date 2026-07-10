# StrokeStyles: Stroke-based Segmentation and Stylization of Fonts

DANIEL BERIO and FREDERIC FOL LEYMARIE, Goldsmiths, University of London, United Kingdom PAUL ASENTE and JOSE ECHEVARRIA, Adobe Research, USA

# (a) (b) (c) (d) (e) (f) （g） (h) (i) P RX

Fig. 1. We stylize glyphs by partitioning them (left, in red) into overlapping and intersecting strokes. (a) We represent strokes as a set of spines with variable width profiles and annotations describing structural relations among strokes. This is then used to reconstruct the glyph in a variety of path-based styles: (b) line-based schematizations, ((c) and (d)) graphic stylizations using skeletal strokes, ((e) and (f )) artistic stylizations that mimic handwriting, and (g) graffiti art. (h) We also use strokes to segment the input into overlapping areas. (i) We use these areas to compute a similarity metric between strokes, allowing consistent shape-based stylizations across the glyphs of a given font.

We develop a method to automatically segment a font’s glyphs into a set of overlapping and intersecting strokes with the aim of generating artistic stylizations. The segmentation method relies on a geometric analysis of the glyph’s outline, its interior, and the surrounding areas and is grounded in perceptually informed principles and measures. Our method does not require training data or templates and applies to glyphs in a large variety of input languages, writing systems, and styles. It uses the medial axis, curvilinear shape features that specify convex and concave outline parts, links that connect concavities, and seven junction types. We show that the resulting decomposition in strokes can be used to create variations, stylizations, and animations in different artistic or design-oriented styles while remaining recognizably similar to the input font.

CCS Concepts: • Computing methodologies → Shape analysis; • Applied computing → Media arts;

Additional Key Words and Phrases: Font structure, stroke-based representations, glyph stylization, junction types, curvilinear shape features, augmented medial axis

ACM Reference format:

Daniel Berio, Frederic Fol Leymarie, Paul Asente, and Jose Echevarria. 2022. StrokeStyles: Stroke-based Segmentation and Stylization of Fonts. ACM Trans. Graph. 41, 3, Article 28 (April 2022), 21 pages. https://doi.org/10.1145/3505246

## 1 INTRODUCTION

Modern fonts are commonly represented as vector outlines. While this format is convenient for exchange, rendering, and printing, it makes it difficult to apply modifications or stylizations that are based on the structure of the glyphs [Campbell and Kautz 2014]. The visual conventions used in creating a font or glyph can be traced back to their origins in stroke-based handwriting and calligraphy [Noordzij 2005], in which a stroke typically embodies a trace of ink on paper left by the gesture of a calligrapher manipulating a brush or pen. The outline of a glyph often conceals a latent structure of generalized strokes that, when combined, closely reproduce the glyph’s shape. Recovering this underlying structure makes it easier to stylize and modify glyphs consistently across an entire font.1

## 1.1 Motivation

Generating fonts in a variety of styles, while leaving sufficient parametric control to a user, is a well-known ill-posed problem [Hofstadter 1982]. Our goal is to capitalize on the wealth of

# AAI Λ Aa

Fig. 2. The targets for our method are glyphs that have a recoverable stroke structure, such as the first three glyphs from the top left (Rockwell, Giddyup and Apollo ASM fonts), but not the glyph on the right (Rosewood). The inferred stroke reconstruction can be exact (Rockwell, Giddyup) or deviate slightly from the glyph’s outline (Apollo). Our method works with glyphs having nonstandard structures, like Giddyup and Apollo, which would present challenges for template-based approaches. In the second row are stylizations of the first three glyphs, produced by our system with constant-width skeletal strokes [Hsu et al. 1993].

publicly available fonts as a source for possible letter structures and styles. By segmenting the glyphs of a font into strokes and characterizing their topological relationships, we produce a scaffold for generating structurally aware stylizations of the glyphs, and the wide variety of available digital fonts becomes the source for these scaffolds (Figure 1).

Our system relies on well-studied principles from visual perception [Wagemans et al. 2011]. It must deal with the same issues raised by the related problem of decomposing two-dimensional (2D) object outlines into parts: multiple ambiguous hypotheses are acceptable, and their selection depends on subtle perceptual cues [De Winter and Wagemans 2006], on domain knowledge, and on functional or causal attributes [Spröte et al. 2016]. In particular, psychophysical results suggest that perceptual grouping [Brooks 2015] and formulating early part-segmentation hypotheses [Xu and Singh 2002] are low-level processes that occur pre-attentively or at least very early in the vision process.

To approximate and model these perceptual processes, we adopt a recently introduced representation of curvilinear shape features based on local symmetry axes, and we identify pairwise relations between these features, called links, that guide the segmentation. We constrain the space of possible solutions by defining seven types of junctions, an intermediate representation of how symmetry axes intersect, that help characterize where and how strokes can overlap or end. Junctions are found iteratively and their identification fully characterize the recovered stroke structure of the glyph.

Our method produces plausible stroke-based segmentations of glyphs, using shape analysis alone (Figure 2). While this can produce segmentations that are somewhat different from the traditional structure of the glyph, or from ground truth if it exists, it has the considerable advantage of being agnostic to the symbols used and works with glyphs that do not match any standard structure for a letter. The result is a system that can be applied to most glyphs and languages and even to other 2D shapes that can be closely approximated by a series of strokes.

This article contains many symbols; we have included a list of them in Appendix D.

## 2 RELATED WORK

Font stylization and synthesis. Some font stylization methods operate on glyph outlines [Campbell and Kautz 2014] or on raster glyph images [Azadi et al. 2018; Haines et al. 2016]. Other approaches operate on glyph structures like we do but rely on a userguided segmentation or skeleton assignment [Gingold et al. 2008]. Suveeranont and Igarashi [2010] use a skinning approach to assign a user-defined structure to font glyphs and then propagate changes made to the skin or skeleton of one glyph to newly generated ones. With a similar objective, Phan et al. [2015] rely on a userguided segmentation of the input glyphs into parametric strokes, defined according to the model of Jakubiak et al. [2006], and then use a probabilistic approach to propagate changes made to parts of one glyph to the rest of its font. Unlike these works, which address style transfer from one glyph to an entire font, we use stroke decomposition as input to structural stylization methods that can apply to an entire font. Our aim is closer to the work of Zhang et al. [2017], who stylize text by subdividing its letters into parts and reconstructing each part with a deformed vector image. The segmentation produced by our method could be used for similar applications.

Other related works use segmentation to create new glyphs or fonts. Xu et al. [2012] use a semi-automatic segmentation procedure to extract strokes from Chinese calligraphy instances and apply a brush model to synthesize new characters based on weighted interpolation. They then train a neural network to guide the synthesis process, based on the supervision of expert calligraphers. Lake et al. [2015] use a probabilistic programming approach to infer plausible motor programs from bitmap images of handwriting and then generate new exemplars by synthesizing novel motor plans. Their approach relies on an automatic thinning-based stroke segmentation method that unfortunately does not perform well with fonts. The output of our method can similarly be interpreted as a motor plan. Such a motor plan can then be modified, for example using the approach of Berio et al. [2017], to produce calligraphic-like glyph stylizations.

Parametric and stroke-based font models. Latin fonts are usually defined with outlines [Karow 1994], but a stroke-based representation of electronic fonts can be traced back to the MetaFont system [Knuth 1979]. It defines glyphs using raster shapes swept along splines. Jakubiak et al. [2006] similarly describe glyph parts using Bézier stroke paths paired with variable-width offsets. Hsu and Lee [1994] show examples of skeletal strokes used in instances of Chinese calligraphy; we also demonstrate how the same method can be used to stylize arbitrary fonts. Hu and Hersch [2001] present a parametric component-based representation of glyphs and emphasize that treating separately each side of a stroke, with respect to a central spine or axis, produces more aesthetically pleasing results. We follow a similar asymmetric approach using the stroking method by Berio et al. [2019], which mimics the appearance of graffiti art. Cox et al. [1982] present a graph-based description of fonts consisting of strokelike parts and their topological relations. Our method captures similar topological relations among strokes.

Decomposition into strokes. Decomposing East Asian characters, which are often based on a hierarchical structure of radicals and strokes, has been well studied [Chen et al. 2017; Sun et al. 2014; Wang et al. 2002] and extensive datasets are available for datadriven methods. However, such methods usually fail with Western fonts and glyphs, which have a wider range of stylistic variations and decorations and which often blend components into each other in ways that make segmentation difficult. For example, Hofstadter [1982] reflects on the countless forms and structures that a single letter can assume. This ill-posed problem [Lamiroy et al. 2015] has been partially addressed with user-defined templates [Balashova et al. 2019; Herz et al. 1997; Phan et al. 2015; Suveeranont and Igarashi 2010; Zhang et al. 2017] or a detailed analysis of glyph outlines [Shamir and Rappoport 1996].

A related problem is decomposing objects other than glyphs into parts. Existing methods address this for applications in graphics [Jiang et al. 2013; Luo et al. 2015; Mi and DeCarlo 2007] and recognition [Macrini et al. 2008]. Recently, with an approach to outline segmentation sharing some similarities with ours, Papanelopoulos et al. [2019] use the exterior medial axis branches to identify some concavities in an outline and then decompose this outline into parts. However, these branches can miss features [Belyaev and Yoshizawa 2001] that are important to stroke decomposition (see Figure 4), a problem that we address in our work.

Very few methods consider the problem of potentially overlapping parts. With the aim of vectorization, Luo et al. [2015] and more recently Kim et al. [2018] propose a data-driven method that can vectorize overlapping parts of Chinese characters, but their methods are not easily applicable to our context, since we are interested in segmenting fonts for which no ground truth is available. Froyen et al. [2015] propose using a Bayesian Hierarchical Clustering method [Heller and Ghahramani 2005] for the segmentation of simple tubular objects with a mixture of splines paired with Gaussian thickness profiles. Favreau et al. [2016] propose another approach that uses a Monte Carlo exploration method to create vectorizations of line drawings that maximise a tradeoff between simplicity and reconstruction accuracy. However, neither method is applicable to the thicker, complex shapes found in fonts. The problem of disentangling potentially overlapping parts also relates to multi-manifold learning [Arias-Castro et al. 2017; Deutsch and Medioni 2017; Goldberg et al. 2009], which is the segmentation of data generated by multiple, potentially intersecting manifolds. While these methods operate on data samples rather than outlines, we use some ideas similar to those developed by Deutsch and Medioni [2017].

## 3 OVERVIEW

Given a 2D glyph generated with a union of strokes, we target the inverse problem of recovering the strokes from the glyph outline. In this context, we consider a stroke to be an elongated 2D region as created by a drawing or painting gesture between two positions on a drawing surface [Noordzij 2005]. The recovered strokes when combined must reproduce the original glyph, providing good coverage of its interior 2D area; this implies that our method can also apply to other 2D shapes that can be well approximated by the union of strokes (Figure 20). Figure 3 shows an overview of our system.

![](images/8cfc6fd3eb3b8dce4d4ae49f026f42c493abd6d97c3dde095de095d98fc8a188.jpg)  
Fig. 3. High-level overview of the segmentation and stylization of a glyph.

Our method relies on a joint analysis of the glyph outline and its interior and exterior medial axes, a hybrid approach that brings together geometry and topology. We use the interior medial axis to describe the glyph topology, while both the interior and exterior medial axes allow us to compute a series of curvilinear shape features (CSFs), descriptors of concave and convex geometric features with associated support segments along the outline (Section 4).

We connect pairs of concavities through line segments that we call links, where each such link represent a potential location where a stroke can start crossing a region covered by multiple strokes (Section 5). Links are then paired to connect a stroke across such a region. The relevance of a given pair of links is measured via a perceptually inspired metric of good continuation along disjoint outline segments.

We use CSFs and links to transform the interior medial axis into a set of strokes, a transformation that is driven by the identification of features that we call junctions (Section 6). Junctions capture semantic stroke attributes by relating branching regions of the interior medial axis to features along the outline like corners and tips. They also characterize regions where strokes may cross and overlap each other. We identify junctions iteratively with a procedure (Section 7) that is driven by the good continuation metric and a set of measures aimed at reproducing the glyph outline while producing strokes that are smooth and perceptually consistent with configuration of concavities along the outline and their relations to the branching features of the medial axis. Junctions produce two stroke representations (Section 8), one consisting of spines paired with variable width profiles (Figure 1(a)) and one consisting of potentially overlapping areas of the glyph that correspond to different strokes (Figure 1(h)).

We use strokes and junctions to generate varied stylizations of a glyph (Section 9), ranging from painterly and decorative effects with skeletal strokes to effects that mimic the appearance of calligraphy or graffiti art to animations. These stylizations can be generated in real time, giving the user a powerful way to explore and interactively adjust different visual results.

## 4 SHAPE ANALYSIS: OUTLINE AND AXIAL FEATURES

Perceptual studies show that 2D shape understanding is driven by a combination of low-level cues from the boundary and interior local symmetries and high-level global properties like the relationships among parts [De Winter and Wagemans 2006]. Motivated by these studies, we begin by constructing interior and exterior medial axes [Blum 1973], denoted $\mathbb { M } ^ { I }$ and $\mathbb { M } ^ { E } ,$ that provide geometrical and topological information about the shape of a glyph (Section 4.1). The medial axes let us identify a set of CSFs that characterize concave and convex segments along the outline (Section 4.2) and facilitate the analysis of outline features such as tangents at concavities (Section 4.2.2). CSFs also map concave outline segments to axial features called ligatures (Section 4.3), portions of $\mathbb { M } ^ { I }$ that might need adjustment to recover smooth strokes. Furthermore, CSFs faciliate identifying outline features in relation to the branching structure of $\mathbb { M } ^ { I }$ (Section 4.4), which will help identify partition line segments called links and topological features called junctions, both needed to correctly find where and how strokes overlap.

## 4.1 Medial Axes

Many algorithms for computing the medial axis exist; we use the discrete Voronoi-based approximation method of Ogniewicz and Ilg [1992], because it is well established and robust. We first densely sample each glyph outline to generate ordered sequences of points $x _ { i }$ and use the polylines that connect the points as an approximation of the outline. We use the authors’ chord residual regularization to discard small spurious medial axis branches that come from discretization. Because the input to the Voronoi-based method is point samples, the medial axes always consist of planar graphs made of polylines connected by vertices $y _ { j } .$ The interior medial axis $\mathbb { M } ^ { I }$ acts as a descriptor of the topological structure of the 2D shape and is used to identify salient convexities, while the exterior medial axis $\mathbb { M } ^ { E }$ is used to identify salient concavities (Section 4.2).

4.1.1 Terminals, Forks, Branches, and Contact Regions. Terminals in the medial axis are vertices of degree one. Forks are vertices of degree three or more. Terminals correspond to curvature extrema or sharp corners of the outline, while forks correspond to potential branching structures of the original shape and to polygonal stroke ends. Forks with degree more than three occur only in highly symmetric configurations, like the center of a square; we remove them by making small perturbations to the outline points. A branch is a series of end-to-end connected edges that begins and ends at a terminal or a fork, with interior vertices of degree two.

Each vertex of a medial axis has an associated contact disk with a radius that is the minimum distance from the vertex to the outline. Each disk associated with a fork is connected to the outline at three distinct points. A terminal vertex has an associated terminal disk and terminal branch. Each terminal disk has a contact region, which is the arc of the disk that approximates the polygonal shape outline to within a small tolerance. We use its midpoint as the representative curvature extremum. Such an arc reduces to a point at a sharp corner where the terminal branch touches the outline. All vertices of degree 2 have disks touching the outline at two distinct points. We often visualize ribs that connect such vertices to the outline.

![](images/cb49f77ec25d9de6451eab187a167fc497d7e70d02df7e9b7d8c733dad159672.jpg)  
Fig. 4. (a) Four successive CSFs with contact regions in black and with support segments, terminal disks and local symmetry axes in color. The pink CSF is a corner and thus has a contact region reduced to a point. Note that the local symmetry axes can intersect and overlap, unlike medial axes. (b) Axes $\mathbb { M } ^ { I }$ (blue) and $\mathbb { M } ^ { E }$ (red), and the resulting convexities and concavities found at branch terminals. (c) Local medial axes are computed over the support segments highlighted in red (concave) and blue (convex), giving two new CSFs. These features are missed in (b), because they do not occur at terminal branches of the medial axes.

4.1.2 Branch Salience, $\beta ( b , f )$ . To distinguish between $\mathbb { M } ^ { I }$ ,branches that characterize the body of a stroke from those that identify morphological features like the cap of a stroke or a corner, we define the salience of a branch b protruding from a fork $f .$

![](images/c997476dc0378c479832d99628e254798e58284e0e89cb20e5e81974e5976704.jpg)

We consider the length s of the outline segment that connects two points $x _ { i }$ and $x _ { j }$ that have ribs connecting to the fork, and that contains at least two other points with ribs con-

necting to the branch’s other endpoint. The branch salience is a measure of “stick-out” [Hoffman and Singh 1997] as follows:

$$
\beta ( b , f ) = \frac { s } { \| \pmb { x } _ { i } - \pmb { x } _ { j } \| } ,\tag{1}
$$

which quantifies the length of the outline segment relative to its width at its point of attachment to the fork. A branch b is said to be salient with respect to a fork f if $\beta ( b , f ) ~ \ge ~ \tau _ { \beta }$ . Based on experiments, we found $\tau _ { \beta } = 2 . 3$ , works well. If the outline points .are on different paths, e.g., when b is part of a loop surrounding a hole, then we set $\beta ( b , f )$ to an arbitrarily large value.

## 4.2 Curvilinear Shape Features

Our segmentation procedure requires identifying convex and concave outline regions, including sharp angles at corners. We call these curvilinear shape features, after Berio et al. [2020] (Figure 4).

Definition 4.1 (Curvilinear Shape Feature). A CSF has five elements: (i) a local symmetry axis, (ii) a terminal disk, (iii) a contact region (arc or point), (iv) the associated extremum of curvature, defined as the midpoint of the contact region, and (v) a pair of outline segments on each side of the contact region called support segments, representing the CSF’s region of influence.

Each support segment of a CSF is the portion of the shape outline extending from one end of the $\mathrm { C S F } ^ { \prime } s$ contact region to the beginning of the contact region of the adjacent CSF (Figure 4(a), colored outline segments). Adjacent CSFs always share one support segment and the CSFs for a given outline fully cover that outline. The local symmetry axis of a CSF is the medial axis $\mathrm { o f }$ the part of the outline spanned by the CSF’s contact region and its two support segments (Figure $4 ( \mathrm { a } )$ , thin colored lines). Because this outline portion is left open, the symmetry axis starts at the CSF terminal disk center and extends, in theory, to infinity; in practice we truncate the axis at an enclosing bounding box. For visualization purposes we extend the axis from the terminal disk center to the associated curvature extremum $x _ { c }$ on the outline, represented by the outline sample nearest to the midpoint of the contact region. In the following, we often simply use “concavity” or “convex-$\mathrm { i t y } ^ { \mathrm { 3 } }$ to refer to the CSF associated with the feature and we use the symbol c.

4.2.1 CSF Computation. We can compute an initial set of convex and concave CSFs using the terminal disks of $\mathbb { M } ^ { I }$ and $\mathbb { M } ^ { E }$ . However, this initial set is incomplete, since the medial axis can miss useful convexities and concavities, depending on the local configuration of the outline [Belyaev and Yoshizawa 2001] (Figure 4(b)). We could identify these missing features with the full Symmetry Set [Giblin and Kimia 2003]; but this is difficult to compute and to manage. Instead, we propose a simpler analysis in which we search for additional intermediate local medial axes by visiting each previously identified support segment. For each such open outline segment, we consider the potential additional CSFs produced by new candidate terminal branches. We select as a new CSF the one with smallest terminal disk radius, and only select a concave CSF if its radius is below an experimentally-determined threshold $( r _ { h } ~ = ~ 0 . 1 5 )$ scaled .by the glyph height. The search is iteratively repeated for the pair of newly introduced shorter outline segments. This procedure ends when no new features are identified, which in practice takes one or two steps for most glyphs. More details are in Appendix A.

![](images/fc8ca118fda761e423d70042ceba2e916d109f454e2601235598f4dadfa1deb8.jpg)

4.2.2 Concavity Features. CSFs facilitate the computation of outline features useful for segmentation, such as tangents and normals near concavities. We assign each concave CSF a pair of unit

tangent vectors $t _ { i }$ and $t _ { j }$ (inset, red arrows) at the endpoints $x _ { i }$ and $x _ { j }$ of its contact region and a unit inward normal (blue arrow), n, with orientation $- ( t _ { i } + t _ { j } )$ and terminating at the CSF extremum, $x _ { c } .$ . More details are in Appendix A.

## 4.3 CSF-based Ligatures

A ligature is a medial axis segment with ribs ending at a concavity. This notion was introduced by Blum [1973] and more recently used to identify shape parts [August et al. 1999; Macrini et al. $2 0 1 1 ] . ^ { 2 }$

![](images/ba71bf0c61d7def7d42ccf3871df21959938f0f45f1e5b14652f32eb3750f6cc.jpg)

We use ligatures more specifically to refer to medial axis vertices and segments with ribs that terminate in the contact region of a concave CSF. The inset figure shows several ligatures in red with their associated ribs. A ligature is always con-

tiguous but can contain vertices from more than one branch. The union of the ligatures for a glyph make a set of ligature regions, connected subgraphs of $\mathbb { M } ^ { I }$ consisting of one or more overlapping ligatures. Each ligature region is a mapping from a connected portion of $\mathbb { M } ^ { I }$ to one or more concavities and can be considered to be “glue” that connects perceptually distinct outline parts [Macrini et al. 2011].

## 4.4 Mapping Concavities to Forks via Sectors

![](images/3b6f80ac49479138a68e1a6abdc4ada5754d4e6dabf1103f176db1267852a289.jpg)

The segmentation procedure requires assigning concave CSFs to each fork $f ~ \in ~ \mathbb { M } ^ { \bar { I } }$ and identifying spatial relations such as adjacency and opposition between concavitities and branches incident to $f .$

We formalize these relations by computing three viewpoints for each $\mathbb { M } ^ { I }$ fork $f ,$ shown as black dots in the inset figure, one for each pair of incident branches. Each viewpoint is the midpoint of a circular arc connecting its two branches and centered at $f .$ I f the fork’s disk (dashed circle) intersects both branches (sector 1), then the arc’s radius is equal to the fork’s disk radius; otherwise the radius is the distance between the fork and the endpoint of the shorter branch (sectors 2 and 3).

A sector is a region of the plane that is visible from a given viewpoint without being occluded by any $\mathbb { M } ^ { I }$ branch. We use visibility polygons [Fabri and Pion 2009; Preparata and Shamos 1985] to compute these. Each sector is delimited by two of the branches incident to $f .$ For example, sector 2 in the inset is delimited by the black branches. When a sector contains the extremum of a concavity, we say that the concavity and the two delimiting branches are adjacent $( \mathrm { e . g . }$ , sector $2 ^ { \circ } s$ concavity and the black branches in the inset) while the concavity and third incident branch are opposite.

4.4.1 Concavity Assignment to Forks. We use ligatures to assign zero or one concavity per sector to the sector’s fork $f ,$ resulting in $f$ being assigned up to 3 concavities. A given concavity may be assigned to more than one fork. To perform the assignments, we examine each sector in turn and all concavities adjacent to the sector’s delimiting branches. Our goal is to determine whether one of these concavities can be interpreted as the result of the intersection of two strokes near $f .$ If a concavity produces a ligature that overlaps with both of the sector’s delimiting branches, then we assign it to that sector (Figure 5(a)). If there is no such concavity, then we search for a concavity that can be assigned to the sector by computing a series of radius-standardized distances for all of the concavity’s ligature points.

Definition 4.2. The radius-standardized distance between ligature point ${ \pmb y } _ { i }$ and a disk in $\mathbb { M } ^ { I }$ is $s ^ { 2 } / r ^ { 2 }$ , where r is the radius of the disk and s is the length of the shortest geodesic path through $\mathbb { M } ^ { I }$ connecting ${ \bf \nabla } _ { y _ { i } }$ to the disk center.

![](images/4b61453ea5d53326146872e21e882b3bcdea898afdeedbf346e3cff8a781cb2a.jpg)  
Fig. 5. Concavity assignment. (a) Three sectors for a fork (black dot), with two concavities shown as red dots assigned to two of its sectors, because they produce ligatures that overlap both of their adjacent branches. (b) The third sector (in blue) contains a concavity (grey dot) that is not assigned, because it is closer, in a radius-standardized sense, to a point ${ \pmb y } _ { e }$ with a rib terminating at the extremum of a convex CSF (black cross). (c) In another case, a sector (yellow) contains multiple concavities and it is assigned the red concavity. The point ${ \pmb y } _ { e }$ is located at the path endpoint, because the disks of the first two forks overlap. Placing ${ \pmb y } _ { e }$ at the second fork along the red path would result in the sector not being assigned any concavity.

For each ligature point, we compute two radius-standardized distances: $d _ { f } ,$ which is computed with respect to the fork’s disk, and $d _ { e } ,$ which is computed with respect to another disk, centered at a point ${ \pmb y } _ { e }$ along the shortest path in $\mathbb { M } ^ { I }$ that connects the $\mathbb { M } ^ { I }$ branch containing the ligature point to the fork. To identify ${ \bf \nabla } y _ { e } ,$ we traverse the path starting from the fork towards the ligature and conclude the search if either (i) we encounter a point that has a rib terminating at the extremum of a convex CSF that is not contained in the sector (Figure 5(b)) or if (ii) we encounter the path endpoint or a fork whose disk does not overlap with the disk of the originating fork or of any previously visited fork (Figure 5(c)). Case (i) helps to distinguish concavities that are opposite convexities and that characterize a smooth bend rather than a potential intersection between strokes. Case (ii) helps to disambiguate nearby forks that potentially share the same concavity assignment with f . A concavity is assigned to the sector if $d _ { f } \leq d _ { e }$ for any of its ligature points and if the geodesic path length $s _ { f _ { \mathrm { m a x } } }$ going from the fork f to the concavity’s last ligature point is shorter than similar geodesic paths for any other concavity (Figure 5(c)).

## 5 PAIRING CONCAVITIES WITH LINKS

Past work has shown that pairs of concavities provide important cues for segmenting object silhouettes into parts [De Winter and Wagemans 2006]. Different approaches use such pairs to define “partition lines” [Luo et al. 2015; Singh and Hoffman 2001] or “cuts” [Papanelopoulos et al. 2019] that delimit perceptually-distinct object parts. Our stroke segmentation problem is related, but it differs in that it requires identifying incidence and crossing relations between potentially overlapping strokes. We start by joining pairs of concavities that we previously mapped to forks with line segments that we call links.

Definition 5.1. A link, denoted η, is a line segment that connects the extrema of two concave CSFs $( c _ { i } , c _ { j } )$ that have been assigned ,to forks, and that is entirely within the glyph.

A single link identifies a potential location where one stroke can intersect or cross another stroke. Furthermore, by pairing links we seek to identify where a stroke enters and exits an ambiguous glyph region, i.e., an area that could be shared by multiple crossing and overlapping strokes.

![](images/fff5a7d948ec9faaaf332ab3b691423c19f8cb0b85f5a6736476aa274282adc9.jpg)  
Fig. 6. Valid link selection. (a) Links that are internal to the shape. (b) Valid links that result in a valid branch assignment and are mutually compatible. (c) Valid links with corresponding salience.

Valid links. A glyph typically contains numerous links, some of which are not helpful, such as the diagonal links in the stem of the $ { ^ { * } \mathrm { { B } } ^ { * } }$ in Figure 6(a). We call the ones that do help valid links (Figure 6(b)). For a link to be valid, it must be possible to assign it a branch and an orginating fork (Section 5.1) that indicate an intersection between two strokes. Furthermore, we consider two valid links to be incompatible if they intersect or have the same branch/fork assignment; otherwise, they are compatible. We call a set of valid links that are mutually compatible a segmentation hypothesis. We choose among segmentation hypotheses using a measure of link salience (Section 5.2), itself in part dependent of a measure of good continuation between concavities (Section 5.3).

## 5.1 Assigning Branches and Forks to Links

A link encodes a direction that can indicate how a stroke protrudes from an intersection with another stroke; we call this direction the link’s flow. We use the flow to search for a branch that emanates from an originating fork in a similar protruding direction. A link is valid only if such a branch can be identified.

## 5.1.1 Flow and Protruding Directions.

![](images/18c73eb5ed36285f4ac03143fed48478e987cef85c1d642affe4ea465d102372.jpg)

Definition 5.2. The flow $\varphi _ { i j }$ (inset: red arrow) for a link (dashed blue) connecting a pair of concavities $C = \{ c _ { i } , c _ { j } \}$ is a unit vec-$\mathbf { \nabla } - ( { \pmb n } _ { i } + { \pmb n } _ { j } )$ , where ,where $\mathbf { } _ { n _ { i } }$ ,and nj are the concavities’ and nj are the concavities' tor with orientation inward normals (yellow arrows).

![](images/a2a4a0956fd990ab35ea09d06fa44688ca79f12c23a998d9a368c780f2f9fe7e.jpg)

Definition 5.3. The protruding direction $\pi ( b , f , C )$ (inset: blue arrow) of a branch b , ,connected to a fork $f$ with respect to a set of concavities C is given by the first unit

tangent vector along the branch that is not part of a ligature (red branch segment) produced by a concavity in C. If the whole branch is part of a ligature, then π is the tangent at $f .$ . A branch connecting two forks has two protruding directions, one for each fork.

Intuitively, the protruding direction uses ligatures to identify a point along a branch that is not shared by multiple strokes and thus can be used to approximate the tangent along a single stroke spine.

A link will be considered for further evaluation only if we can identify a branch b and an originating fork $f ,$ for which the projection, ${ \boldsymbol { \mathit { p } } } ,$ of flow $\varphi _ { i j }$ onto π is strictly positive, where $\mathcal { P }$ is computed as

![](images/2dbde5e97e5310d19715eb7fa8cd3cf25c61fc84558fcd844254937f1a9021b4.jpg)  
Fig. 7. Branch and fork assignment of a link (dashed blue line). A red arrow shows the flow direction, $\varphi _ { i j }$ (Definition 5.2) of the link, while black dots and red segments are forks and branches that could be assigned to that link. Panels (a), (b), (c), and (d) show prototypical branch configurations that result in a normal link. In (d), the concavities are assigned to both the black and the blue fork, but p (Equation (2)) is positive only for the black fork. (e) The link intersects two branches incident to different forks, creating a compound link.

$$
p ( b , f , C ) = \varphi _ { i j } \cdot \pi .\tag{2}
$$

5.1.2 Fork and Branch Assignment. We use Equation (2) to search for a branch b and fork $f$ by considering the forks $f _ { i }$ and $f _ { j }$ that were assigned to the concavities $C = \left\{ c _ { i } , c _ { j } \right\}$ (Section 4.4.1). ,We consider two mutually exclusive cases to identify valid links.

Case 1: Normal link. There is at least one fork $f _ { i }$ that has both of the link’s concavities assigned to it. For each such $f _ { i }$ we identify the branch $b _ { i }$ that delimits both sectors containing the concavities and compute $\mathit { p } ( b _ { i } , f _ { i } , C )$ . If there is more than one such $f _ { i } ,$ then we , ,take the one with the largest positive p and assign $( b , f _ { i } )$ to the link. ,Figure 7(a)–(d) show four prototypical configurations resulting from such an assignment.

Case 2: Compound link. There is no fork that has both concavities assigned to it and the link intersects two or more branches (Figure 7(e)). We define $F _ { B }$ to be the set of forks at the endpoints of the intersecting branches. We then consider each $f _ { i } \in F _ { B }$ and find the branch $b _ { i }$ with maximum projection $\textstyle p ( b _ { i } , f _ { i } , C )$ among , ,branches incident to each fork. If (i) all the projections $\mathit { p } ( b _ { i } , f _ { i } , C )$ are positive, then (ii) all the branches $b _ { i }$ , ,are non-salient, (iii) none of the branches share a fork, (iv) each branch $b _ { i }$ has ribs terminating in only one concavity in $C ,$ and (v) each fork $f _ { i }$ has a disk that overlaps with the disk of another fork in $F _ { B } ,$ this results in a special configuration we call a compound link. Then, the link is assigned any one of these branches together with its fork. This configuration is similar to a normal link, except that the protrusion is not sufficient for the branches to merge at a single fork (compare Figure 7(d) and (e)).

## 5.2 Link Salience

The disambiguation of incompatible links can be achieved with a measure that prioritizes perceptually salient links. We use three concepts from perceptually driven studies of part decomposition to favor links that are as follows: (i) short (or the “short-cut rule” [Singh and Hoffman 2001; Singh et al. 1999]), (ii) located between outline regions with good continuation (or “limbs” [Siddiqi and Kimia 1995]), and (iii) connecting pairs of concavities with a relatively small radius of curvature (or the “minima rule” [Hoffman and Richards 1984]). Link salience is then computed as

$$
\omega ( \eta ) = e ^ { - ( r _ { 1 } + r _ { 2 } ) / ( 2 r _ { \mathrm { m a x } } ) } + \psi ( c _ { 1 } , c _ { 2 } ) ,\tag{3}
$$

![](images/ebb09658fb7a0b5700406707dfacc3aea24b0a853f289e91e9b9c917707e0a96.jpg)  
Fig. 8. Association fields for two concavities in a letter T with corresponding colored values $\psi .$ The tangents pointing to the right are colored according to their association with the black tangents. (a) Case where the corners are well aligned and the association field gives a sufficiently high good-continuation value $\psi \approx 0 . 7 5 .$ (b) Case where the corners are not well .aligned: The association field from one corner reaches the other but only with a low good-continuation value $\psi \approx 0 . 2 5 .$

combining an exponential function that decays with increasing concavity radii $r _ { 1 } , r _ { 2 } $ , scaled by the maximum concavity radius $r _ { \mathrm { m a x } } ,$ ,, together with a measure of good-continuation between the linked concavities, denoted $\psi ( c _ { 1 } , c _ { 2 } )$ , that decays with the distance ,between concavities and thus penalizes longer links.

## 5.3 Good Continuation (ψ ) for Links

Selecting valid links requires pairing concavities using a measure of good continuation along the outline. We use association fields [Wagemans 2018], which have been proposed to model the neural processes responsible for contour integration and perceptual grouping in early vision. A few computational implementations have been defined, the original one being based on cocircularity [Parent and Zucker 1989; Yen and Finkel 1998], i.e., how one local orientation, typically specified by an edge, can be connected to another nearby edge if it is reachable by circular paths within a region specified by the field. We adapt a more recent experimentally verified approach by Ernst et al. [2012] that is based on a stochastic model of contour integration [Williams and Thornber 2001]. Given two oriented edge elements, the model defines a field that decays as a Gaussian function of deviation from perfect cocircularity, collinearity, and distance between the two edges (Figure 8).

We compute the good-continuation value $\psi ( c _ { i } , c _ { j } )$ for a link’s ,two concavities by first selecting the outline tangent at an endpoint of each concavity (Section 4.2.2) that is most orthogonal to the link’s flow $\varphi _ { i j }$ (Definition 5.2). The association field is then computed using the concavity endpoints and tangents and set to decay exponentially with distance relative to a spread parameter, $\sigma _ { d } ,$ which we set to $2 r _ { \mathrm { m a x } }$ , i.e., twice the maximum radius of any $\mathbb { M } ^ { I }$ disk that is not part of a ligature region. More details are in Appendix B.

We will also evaluate a good continuation measure $\psi$ in two other cases: (i) when selecting the best crossing paths for strokes, such that a stroke can enter and exit an ambiguous glyph region, by comparing pairs of links (Section 7.2), and (ii) when associating stroke spines (Section 7.3.2). Before we reach those cases, using links and their assigned concavities, we need to categorize all $\mathbb { M } ^ { \Breve { I } }$ forks and their incident branches into higher-level features we call junctions.

## 6 JUNCTIONS

A junction γ comprises a set of $\mathbb { M } ^ { I }$ forks $F _ { \gamma }$ together with their assigned links and concavities. It defines a configuration of $\mathbb { M } ^ { I }$ branches that correspond to a particular area in the glyph. For brevity, we will say that the junction covers these branches and forks. Once all junctions have been identified, they uniquely determine the inferred stroke decomposition of a glyph. Note that we use “junction” to refer to $\mathbb { M } ^ { I }$ branches joining, and not to glyph strokes joining. Junctions often coincide with areas where strokes join, but not always.

![](images/cad7c785dcfc5e8332e82a88baef364e8fa1199bc4227c5634f8f9fc7672aa2f.jpg)  
Fig. 9. Junctions. The first row shows each fork (black dot), branch (thick colored path), concavity (red dot), and link (dashed segment) configuration that characterizes each junction type. The second row shows the resulting strokes. (a) Two half-junctions, defined by two link pairs (dashed blue and pink) that share the same multitraced crossing path that connects the same forks (black dots). The two junctions produce two crossing strokes. (b) One T-junction, defined by one link (dashed blue). (c) One Y-junction, defined by a concavity opposite a root branch. (d) One L-junction, with the root in grey and its hierarchy (lighter grey), which will be discarded. (e) Stroke end. (f ) Protuberance, characterized by a compound link (dashed blue). (g) Three null-junctions leading to a single stroke.

We define a taxonomy of seven junction types (half, Y, T, L, stroke end, protuberance, and null), shown in Figure 9, sufficient for our goal of stroke stylization.

## 6.1 Junction Types

Half-junctions. One stroke goes across one or more other strokes. A half-junction is characterized by a pair of links that are assigned to different forks and have a high good-continuation value between the concavities at the link ends (Figure 9(a)). Unlike the other junction types, which identify one or two strokes with all branches incident to one fork, a half-junction identifies one stroke that connects two branches and enters and exits a region delimited by the links. This simplifies the analysis of complicated crossings with more than two strokes. A simple crossing like that in Figure $9 ( \mathrm { a } )$ consists of two half-junctions that cover the same forks. Any additional stroke crossing the same area would imply an additional half-junction. The crossing path of each half-junction is the shortest sequence of branches in $\mathbf { \widehat { M } } ^ { I }$ connecting the forks assigned to the links.

T-junctions. One stroke is incident to another in a nearperpendicular fashion. A T-junction is characterized by a link that identifies a branch protruding from a fork (Figure 9(b)).

Y-junctions. Two strokes branch out of an overlapping region. A Y-junction is characterized by a representative concavity c that is assigned to a fork $f$ and that is opposite to a salient root branch incident to f (Figure 9(c)).

L-junctions. One stroke contains a corner or an elbow-like bend (Figure 9(d)). L-junctions have a configuration similar to Yjunctions, with a representative concavity opposite a root branch, but this root is short and often not salient.

![](images/78bc68c28334734674d6510cc09b651ab78babd6f90d870a9734c0b322451565.jpg)  
Fig. 10. Recovering strokes for a letter $^ { * } \mathsf { A } . ^ { * }$ (a) Structural operations on the stroke graph S with vertices $( \mathbb { M } ^ { I }$ branches) shown as red dots and edges as red arcs. The arcs connect branches that are combined into a single stroke. (b) Adjustment operations on the stroke segments: blue strokes with black spines are before adjustments, while black strokes with white spines are after adjustments. Each step straightens curved strokes near a junction; in the first step the effect is very subtle.

Stroke-ends. The $\mathbb { M } ^ { I }$ branching structure at the junction is a tree composed of non-salient branches and is associated with the end of a stroke (Figure 9(e)).

Protuberances. The $\mathbb { M } ^ { I }$ branching structure is nested with one of the non-salient branches being assigned to a compound link (Figure $9 ( \mathrm { f } ) )$ .

Null-junctions. $\mathbb { M } ^ { I }$ contains a fork arising from a small or noisy outline feature (Figure $9 ( \mathrm { g ) ) }$ .

## 6.2 From Junctions to Strokes

Junctions identify semantic stroke features while also helping determine how $\mathbb { M } ^ { I }$ branches are transformed into strokes. To drive this transformation, we create a stroke graph S in which each vertex is a $\mathbb { M } ^ { I }$ branch and each edge connects branches that are part of the same stroke. Each vertex in S is also associated with a stroke segment, a spine and a width profile that initially coincide with the the path of the branch in $\mathbb { M } ^ { \hat { I } } ,$ and the union of the disks for that branch. The vertices in S are initially set to be disconnected. We identify junctions one by one, and with each identification we perform structural operations (Section 6.2.1) on the connectivity and structure of S and adjustment operations (Section 6.2.2) on the associated stroke segments. Which operations are performed is a function of the junction type (Section 6.2.3). We will describe the identification procedure in detail later, in Section 7, after discussing the different junction types in more depth and how these transform $\mathbb { M } ^ { I }$ into strokes.

![](images/c58c48697fa189f4f2c0e6a2fabb0116ba41de812ee42ba5c108a54e5a24d9f5.jpg)  
Fig. 11. Operations on the branches and connectivity of S. (a) Connecting two branches incident to the same fork (black dot). (b) Multitracing (duplicating) a branch. (c) Discarding two branches and the treelike hierarchy attached to one of them.

Once all junctions have been identified, the stroke segments for each connected component of S map to one stroke in the glyph. Figure 10 shows the steps in the segmentation of a single glyph. Each step shows the changes to the stroke graph and the adjustments to the stroke segments.

6.2.1 Structural Operations on S. Identifying a junction leads to applying one or more of the following structural operations to S:

• Connect two or more $\mathbb { M } ^ { I }$ branches: Add edges between pairs of vertices in S. The corresponding $\mathbb { M } ^ { I }$ branches are incident, and will be part of the same stroke (Figure 11(a)).

• Multitrace one or more $\mathbb { M } ^ { I }$ branches: Duplicate the corresponding vertices in S. This will let an $\mathbb { M } ^ { I }$ branch be shared by more than one stroke (Figure 11(b)).

• Discard one or more branches incident to the same fork: Remove them from S. This removes branches that are not relevant to constructing a stroke. The operation is similar to conventional medial axis pruning methods [Shaked and Bruckstein 1998] and is applied recursively to any attached tree-like hierarchy in $\mathbb { M } ^ { I }$ . It ends when it encounters a branch already connected in S (Figure 11(c)).

6.2.2 Adjustment Operations. Transforming the connected components of S into strokes involves assembling a simple path for each component, starting from a degree 1 vertex in S if it exists, or from an arbitrary vertex if the path forms a loop. Recall that the paths in S begin as the paths of the $\mathbb { M } ^ { I }$ branches. To recover smooth strokes from these paths, we must remove distortions that often occur near ligature regions. We use transitions that replace portions of one or more stroke segments with ones that smoothly interpolate an initial and a final pair of centers and radii, $( \pmb { y } _ { i } , \pmb { r } _ { i } )$ and $( { \pmb y } _ { j } , r _ { j } )$ . We define two transition types:

• A smooth transition has a spine with points sampled from a clothoid connecting ${ \pmb y } _ { i } \mathrm { t o } { \pmb y } _ { j }$ and disk radii given by linearly interpolating between $. r _ { i }$ and rj . The parameters of the clothoid are determined by estimating a pair of tangents $( t _ { i } , t _ { j } )$ coinciding with ${ \pmb y } _ { i }$ and $y _ { j }$ ,(Figure 12, top row) and then using a secant-based optimization method by Levien [2009]. If not stated otherwise, then $r _ { i }$ and $r _ { j }$ are also assumed to be the disk radii at ${ \pmb y } _ { i }$ and $y _ { j }$ . Note that in many cases this clothoid reduces to a straight line segment.

![](images/68ff0b9e71d2ff0c5539e0914d3378bf8346fc7e28842c0520994fd7f2269314.jpg)  
Fig. 12. Disk adjustment operations with a smooth transition (top row) and a straight transition (bottom row). (a) Branches (color coded) and disks (blue) before adjustment. (b) Ligature (in red) being replaced by the transition. The black dot in the second row is the endpoint of the straight transition. (c) Adjusted branch and disks.

• A straight transition has a straight spine that connects ${ \bf \nabla } _ { y _ { i } }$ and $y _ { j }$ and a constant width profile $r _ { i } = r _ { j } = r$ (Figure 12, bottom row).

6.2.3 Junction Operations. Each junction type determines a series of structural and adjustment operations that transform S into strokes.

Half-junctions. A half-junction multitraces the branches that fall along the crossing path and then connects the multitraced branches with the branches protruding from the two links. The junction adjusts the stroke segments associated with these branches with a smooth transition. The transition starts and ends at the limits of the ligature region produced by the junction’s linked concavities.

T-junctions. A T-junction connects the two non-protruding branches incident to the fork and adjusts the associated stroke segments with a smooth transition. The junction also adjusts the stroke segment associated with the protruding branch with a straight transition. The transition extends the segment so it terminates at the intersection with the path produced by the smooth transition.

Y-junctions. A Y-junction connects the root to one of the other branches and leaves the otherbranch smoothly protruding from the connected (2) (4) path (inset, 1, 2). The choice of which branch is connected depends on the junction identification procedure detailed in Section 7.3. Other interpretations are possible: 3, with a multitraced root, and 4, with three separate strokes. We find that the first two are sufficient for our stylization purposes, but others might be useful in other scenarios. The junction adjusts the connected stroke segments with a smooth transition and the protruding one with a straight transition. Both transitions replace the ligature produced by the concavity and the disks centered within the fork.

![](images/d9568c0bfdd3989d06bb6bc5670c49ba085d0aa43ffe5861f2837e31f784e47f.jpg)

L-junctions. An L-junction discards the root branch, connects the other two branches and adjusts the corresponding stroke segments with straight transitions that meet at a common point of intersection. The transitions have a constant radius $r _ { i } = r _ { j }$ determined by the radii at the edges of the ligature produced by the concavity.

Stroke-ends. A stroke-end discards the two least salient branches incident to the fork along with any attached branch hierarchies, and adjusts the third branch with a straight transition that extends the fork to a location near the outline.

Protuberances. A protuberance adjusts the branch assigned to the compound link with a straight transition and discards all the other non-salient branches associated with the link for which Equation (2) is positive. The junction also connects the branches incident to the discarded ones.

Null-junctions. A null-junction discards the least salient branch incident to the fork and connects the other two branches incident to the fork.

## 7 JUNCTION IDENTIFICATION

Junctions often occur in complex and nested configurations and their identification becomes non-trivial. Similar to existing approaches for part decomposition [Papanelopoulos et al. 2019; Siddiqi and Kimia 1995], our identification method uses an iterative approach (Figure 10) consisting of four main steps. First, we identify protuberances associated with compound links. Second, we use good continuation to identify half-junctions that cover forks in a single ligature region. We process these junctions early, since they identify crossing paths that should not be disconnected by other subsequently identified junctions. Third, we identify all the remaining junction types by examining one $\mathbb { M } ^ { I }$ fork at a time. Fourth, we examine pairs of previously identified T-junctions, transforming some into half-junctions if the corresponding links have high good continuation value.

Auxiliary graph H. Identifying a junction can be interpreted as recovering a part of a stroke, and this can change which concavities and links are meaningful for identifying the next junction. To manage these changes we use a graph $\mathbb { H } = ( C , H )$ having one ver-,tex per concavity and one edge per valid link. Each iteration of the identification procedure removes vertices (concavities) and edges (links) from H depending on the identified junction. Removing a vertex also removes all incident edges, affecting the subsequent identification of remaining junctions.

## 7.1 Step 1: Identify Protuberances

In the first step, we identify a protuberance from each previously identified compound link. This step does not modify H but it localizes small protrusions, transforming these into small strokes that can later be associated with T-junction or a half-junction, and less often to another junction.

## 7.2 Step 2: Identify Half-junction

Identifying half-junctions requires finding candidate link pairs in H that can be associated based on good continuation.

![](images/61136bf2cf3ba11b191d83d44d8cd3c2b339076431e066fdb5b08ac9b92f56ca.jpg)

For two links ηi and $\eta _ { j }$ having concavities $( c _ { 1 } , c _ { 2 } )$ and $( c _ { 3 } , c _ { 4 } )$ , we define the connecting good-continuation value $\psi ( \eta _ { i } , \eta _ { j } )$ to be the product $\psi ( c _ { 1 } , c _ { 3 } ) \ \times \ \psi ( c _ { 2 } , c _ { 4 } )$ for the non-, ,crossing links connecting the endpoints of $\eta _ { i }$

and $\eta _ { j } .$

Two links $\eta _ { i } , \eta _ { j }$ , can be paired into a half-junction if they do not share a concavity and the connecting good-continuation value $\psi ( \eta _ { i } , \eta _ { j } )$ is greater than a threshold, set experimentally to 0 25.

![](images/8281dd94e9f1ee32ae72d26df3de40edd2210a456ce0f8353d3cc4b8c70b68e7.jpg)  
Fig. 13. Half-junction disambiguation. (a) The red colored links are all part of potential half-junction pairs. The dashed-red links are nested. For example link 3 is nested, because its protruding branch (blue) is part of the crossing path between link 1 and link $^ { 6 , }$ which can be paired. Link 7 (green) is not paired with any other link i, because $\psi ( \eta _ { i } , \eta _ { 7 } )$ ) never exceeds the pair-,ing threshold. (b) This configuration results in two half-junctions produced by the pairs (1 6) and (4 5).

Candidate half-junctions can occur in ambiguous nested configurations. We consider a link in a pair to be nested if it is assigned a branch that is part of any crossing path defined by another pair (Figure 13(a)). If this is the case, then the nested pair is not considered a potential half-junction.

In some glyphs, particularly in hanzi, one stroke crosses another and ends in a short, rounded protrusion (Figure $7 ( \mathrm { e } ) )$ . In this case the tangents at the concavities do not always capture the perceived direction of stroke continuation, but we can detect this, because one of the links ηi or ηj is assigned a non-salient branch. We then re-orient the tangents corresponding to its concavities to match the link flow direction.

We identify an initial set of half-junctions by examining groups of links that are assigned forks that are part of a single ligature region. For each group we identify candidate link pairs $\eta _ { i } , \eta _ { j }$ that ,are consistent with the conditions above and are not nested, and then process these pairs in order of decreasing good continuation $\psi ( \eta _ { i } , \eta _ { j } )$ . We create a half-junction only if a pair does not include a previously processed link.

7.2.1 Updating H. Every time we identify a half-junction, we remove its two links from H. We also remove any link that is assigned a branch that shares more than one vertex with the crossing path. This guarantees that the path will not be disconnected by a subsequently-identified junction.

## 7.3 Step 3: Identify Other Junctions

The five other junction types are identified one fork at a time with a procedure that depends on the links $H _ { f }$ and concavities $C _ { f }$ assigned to a given fork $f ,$ both of which are in H. Our goal is to select a junction $\gamma$ for f that produces a good approximation of the glyph near $f ,$ while also producing strokes that are smooth and consistent with the configurations of concavities $C _ { f }$ and links $H _ { f }$ . We evaluate a potential junction using the following four measures:

(1) Coverage, $\Lambda _ { \mathbb { I } } { \boldsymbol { : } }$ Rewards strokes that provide a good cover of the corresponding glyph region (Section 7.3.1).

(2) Smoothness, $\Lambda _ { \psi } .$ : Rewards T-, Y-, or L-junctions that produce smooth strokes (Section 7.3.2).

(3) Concavity significance $\Lambda _ { w } \colon$ Rewards $\mathrm { T } , \mathrm { Y } -$ , or L-junctions that are consistent with the configuration of concavities in $C _ { f }$ (Section 7.3.3).

![](images/34ba5583f8a995371bfbde919832f2100168f05d2324f1e6b6817abd3abba4c4.jpg)  
Fig. 14. Possible interpretations for the fork in this K (black dot) where the two diagonal strokes, shown in blue, join. (a) The blue area also shows the before-adjustment area used in the coverage calculation and the most salient concavity (red dot). The darkened areas in the remaining subfigures show the adjusted strokes. (b) The T-junction interpretation has the highest score and so is the one selected. ((c) and (d)) The most salient concavity (red dot) is below the fork (black dot), leading to the root for the two Y-junction interpretations being the branch that extends to the upper right. (e) It also forces the L-junction’s corner, which must be opposite the most salient concavity, to be in the upper right and forcing the implausible structure shown. (f ) In the stroke-end interpretation, the entire branch hierarchy to the right of the fork is evaluated as an elaborately flared end to the short branch connecting the fork to the vertical; because this is not plausible, the score is very low. Note that the two highest-scoring interpretations give the same stroke decomposition.

(4) Link salience $\Lambda _ { \eta } \colon$ Rewards T-junctions that are characterized by a salient link (Section 7.3.4).

Coverage applies to all junction types, while smoothness and concavity significance only apply to T-, Y-, and L-junctions, and link salience only applies to T-junctions.

This class-dependent organization of measures lets us disambiguate junctions without relying on training data [Plamondon and Srihari 2000] but poses the challenge of comparing measures with different ranges [Bailey 2001]. We adopt a heuristic solution akin to the “one-versus-one” classification [Galar et al. 2011] where, given N candidate junctions (Section 7.3.5), we evaluate all $N ( N - 1 ) / 2$ pairwise junction combinations using the terms that /are valid for both junction types (Section 7.3.6). We process forks iteratively with an ordering procedure (Section 7.3.7) that depends on $H _ { f }$ and $C _ { f }$

7.3.1 ΛI: Coverage. For each junction type, we seek to evaluate how well the resulting strokes cover the underlying glyph region. To do so, we consider the connected components of S that include any branch covered by the junction. We then rasterize the associated stroke segments before and after the operations induced by the junction and compute their respective areas $A _ { \gamma }$ and $A _ { \gamma } ^ { \prime }$ (Figure 14). The coverage is computed as

$$
\Lambda _ { \mathbb { I } } = \ln \left[ ( A _ { \gamma } \cap A _ { \gamma } ^ { \prime } ) / A _ { \gamma } \right] .\tag{4}
$$

7.3.2 $\Lambda _ { \psi } .$ Smoothness. For $\mathrm { T } , \mathrm { Y } - ,$ and L-junctions, we reward the junction type that maximizes stroke smoothness. We quantify smoothness as a geometric mean as follows:

$$
\Lambda _ { \psi } = \ln \left[ \left( \prod _ { i = 1 } ^ { M } \psi _ { i } \right) ^ { \frac { 1 } { M } } \right] ,\tag{5}
$$

where M depends on the junction type and $\psi _ { i }$ are good continuation values computed along stroke spines. For T- and Y-junctions, $M = 1$ and $\psi _ { i }$ is the good continuation for the point-tangent pairs used to compute the smooth transition of the connected stroke.

![](images/cb1a760773f4641758b3b5076abd4d57cf4afabe9c961ff27c9308016d52701c.jpg)

For L-junctions, $\begin{array} { l l l } { M } & { = } & { 2 } \end{array}$ and we compute two good continuation values, respectively between the tangents $t _ { i } , t _ { j }$ at the ends ${ \mathbf { \nabla } } y _ { i } , y _ { j }$ of ,the ligature and two other tangents $t _ { k } , t _ { l } ,$ par-

,allel to the junction’s straight transitions (inset, black lines) and anchored at their point of intersection.

For all cases we compute good continuation (Section 5.3) with spread parameter $\sigma _ { d }$ set to the distance between the tangent origins, which results in a measure invariant to distance.

7.3.3 $\Lambda _ { w } \colon$ Concavity Signifiance Measure. The inward normal n at a concavity c is similar to the “process arrow” proposed by Leyton [1988], which captures the direction of a force that produces the concavity when locally applied to an elastic version of the outline.

![](images/44a6dd8fa9263f4c33401547fd825d7f4623b57a1ba0bbb4d3b14e104950e8ba.jpg)

We use this analogy to compute the significance of a concavity c with respect to the fork position $y _ { f } .$ , by assuming that the glyph is made of an idealized linearelastic, isotropic, incompressible mate-

rial with a Poisson ratio of 0 5. Based on Flamant’s solution for a .normal force acting on an elastic half-plane [Kachanov et al. 2003], the normal displacement at $y _ { f }$ produced by a force applied at a point $x _ { i }$ along the contact region and oriented according to n is proportional to

$$
u = - 0 . 5 \ln { \left( \frac { R ^ { 2 } } { L ^ { 2 } } \right) } + \frac { \cos ^ { 2 } \theta } { R ^ { 2 } } ,\tag{6}
$$

where $\theta _ { i }$ is the angle between n and the vector from $x _ { i }$ to yf , R is the magnitude of this vector and L is a constant that determines a distance at which the displacement vanishes [Timoshenko and Goodier 1951]. We use $L = 2 r _ { f }$ , where $r _ { f }$ is the disk radius at the fork. The significance of a concavity c (inset: grey sectors) is then

$$
w ( c , f ) = u / r ^ { 1 / 2 } ,\tag{7}
$$

where r is the CSF radius. Intuitively, high significance for just one concavity in $C _ { f }$ suggests the presence of a Y- or L-junction, while high significance for two such concavities suggests the presence of a T-junction. To quantify this, we sort the concavity significances $w _ { i }$ for the three fork sectors (Section 4.4) in decreasing order, $w _ { 1 } \geq$ w2 $\geq w _ { 3 }$ , setting $w _ { i } = 0$ if a sector has no concavity. We consider their differences normalized by the sum $\Sigma _ { w } = w _ { 1 }$ 1 +w2 +w3 [Westin et al. 2002]. If we are evaluating the junction γi as a Y- or L-junction, then we compute the following:

$$
\Lambda _ { w } ( \gamma _ { i } ) = \ln \left[ ( w _ { 1 } - w _ { 2 } + w _ { 3 } ) / \Sigma _ { w } \right] ,\tag{8}
$$

where a high value of $\Lambda _ { w } ( \gamma _ { i } )$ means that w1 $> w _ { 2 } \simeq w _ { 3 } .$ . If we are evaluating γi as a T-junction, then we compute

$$
\Lambda _ { w } ( \gamma _ { i } ) = \ln \left[ ( 2 w _ { 2 } - w _ { 3 } ) / \Sigma _ { w } \right] ,\tag{9}
$$

where a high value of $\Lambda _ { w } ( \gamma _ { i } )$ means that $w _ { 1 } \simeq w _ { 2 } > w _ { 3 }$

7.3.4 $\Lambda _ { \eta } \colon$ Link Salience. This last measure is simply given by

$$
\Lambda _ { \eta } = \ln \omega ( \eta ) ,\tag{10}
$$

where $\omega ( \eta )$ is the salience of the junction’s link (Equation (3)).

7.3.5 Candidate Junctions. For each fork f we build a set $J _ { f }$ of candidate junctions. Each such set always include a null-junction and a stroke-end, given by the least salient individual branch and the least salient branch pair incident to the given fork $f .$ The other members of ${ \bf \cal J } _ { f }$ depend on the presence and configuration of links and forks assigned to the fork, and on the saliency of the fork’s incident branches.

If $H _ { f }$ (the set of forks assigned to f ) is non-empty, then $J _ { f }$ can contain a T-junction for each link in $H _ { f } . \operatorname { I f } C _ { f }$ (the set of concavities assigned to $f )$ is non-empty, then we consider the two Y-junction configurations and single L-junction produced by the most significant concavity in $C _ { f }$ . The presence of T-, Y-, and L-junctions in $J _ { f }$ depends on the following constraints:

(1) $J _ { f }$ contains a Y-junction only if the root is salient.

(2) $J _ { f }$ contains a $\mathrm { T } \mathfrak { r } , \mathrm { Y } \mathfrak { r } _ { \mathrm { : } }$ , or L-junction only if all the branches incident to the fork, with the exception of the root if present, have saliency greater than a lower bound $\beta _ { \mathrm { m i n } }$

(3) $J _ { f }$ contains an L-junction only if the representative concavity is well aligned with the root, i.e., the dot product between the root protruding direction and the concavity bisector is positive.

(4) Jf contains an L-junction only if the representative concavity has a curvature radius smaller than $\lambda _ { \mathrm { L } } r _ { f } \cos ( \theta _ { c } / 2 )$ , with $r _ { f }$ the fork’s radius and $\lambda _ { \mathrm { L } }$ /a user configurable multiplier experimentally set to 0 5.

Constraint 1 enforces consistency with the Y-junction definition. Constraint 2 functions similarly to a medial axis pruning strategy, but considers junction configurations to determine which $\mathbb { M } ^ { I }$ branches are not significant. We use a lower bound $\beta _ { \mathrm { m i n } } = 1 . 5$ for the examples given. Increasing $\beta _ { \mathrm { m i n } }$ .will make flared stroke ends more likely to be categorized as stroke-end junctions and less likely to be separated as a serif with a T-junction. Constraint 3 avoids certain cases where a concavity being assigned to a fork can result in misidentifying a stroke-end or null-junction as an L-junction. Constraint 4 avoids certain cases in which corners are misidentified as null-junctions. While this last constraint is not critical to the recovery of plausible strokes, it improves stylization results in particular in cases that involve structural modifications of the stroke spines.

7.3.6 Identification. The preference for one junction $\gamma _ { i }$ among a pair $( \gamma _ { i } , \gamma _ { j } )$ is given by

$$
\Lambda _ { i j } ( \gamma _ { i } ) = \Lambda _ { \mathbb { I } } + \delta _ { \mathrm { T Y L } } \Lambda _ { \psi } + \delta _ { \mathrm { T Y L } } \Lambda _ { w } + \delta _ { \Gamma } \Lambda _ { \eta } + \Lambda _ { \gamma } ,\tag{11}
$$

where $\delta _ { \mathrm { T Y L } } = 1$ if both $\gamma _ { i }$ and $\gamma _ { j }$ are one of a T-, Y-, or L-junction, and $\delta _ { \mathrm { { T } } } = 1$ if both are T-junctions. Otherwise, both terms are zero. The last term $\Lambda _ { \gamma }$ lets a user express a preference for the identification of certain junctions types with $\Lambda _ { \gamma } ~ = ~ \ln \lambda _ { \gamma }$ , where $\lambda _ { \gamma }$ is a junction-dependent weight that defaults to 1. We find that it works well to use a slightly lower value of $\lambda _ { \gamma }$ for null-junctions, and a higher value of $\lambda _ { \gamma }$ for T-junctions. This generally favors Ljunctions over null-junctions in certain corner configurations, and favours T-junctions over Y-junctions in the presence of a link. In the examples given, we use $\lambda _ { \gamma } = 1 . 1$ for T-junctions and $\lambda _ { \gamma } = 0 . 9 5$ . .for null-junctions. We finally estimate the probability of selecting a junction $\gamma _ { i }$ among a pair, with

![](images/acd6c3b60c788037dba45b6cd2f4412906b82508e7186566e29393c4a183333e.jpg)  
Fig. 15. Final identification of half-junctions. (a) The glyph region emphasied with the blue circle consists of two strokes that are perceived as crossing and have two separate ligatures. (b) The procedure up to Section 7.4 produces two T-junctions, which results in three strokes; the yellow and blue strokes protrude from the red stroke. (c) The links that characterize the two T-junctions have high good continuation, so the procedure in Section 7.4 transforms these junctions into one single half-junction replacing the previous two strokes (yellow and blue) with a single longer one (blue).

$$
P _ { i j } ( \gamma _ { i } ) = \frac { \exp { \Lambda _ { i j } ( \gamma _ { i } ) } } { \exp { \Lambda _ { i j } ( \gamma _ { i } ) } + \exp { \Lambda _ { i j } ( \gamma _ { j } ) } }\tag{12}
$$

and select the junction $\gamma _ { i }$ that maximises

$$
P _ { i } = \sum _ { 1 > = j \ne i < N } P _ { i j } ( \gamma _ { i } ) .\tag{13}
$$

7.3.7 Iterative Process. We process forks in an order of decreasing priority given by

$$
\left\{ \begin{array} { l l } { \operatorname* { m i n } _ { b \in B _ { f } } \beta ( b , f ) \displaystyle { \operatorname* { m a x } _ { \eta \in H _ { f } } \omega ( \eta ) } \ + 2 K , } & { \mathrm { i f ~ } H _ { f } \mathrm { ~ i s ~ n o n - e m p t y } , } \\ { \displaystyle { \operatorname* { m i n } _ { b \in B _ { f } } \beta ( b , f ) \displaystyle { \operatorname* { m a x } _ { c \in C _ { f } } w ( c , f ) } \ + K } , } & { \mathrm { i f ~ } H _ { f } \mathrm { ~ i s ~ e m p t y ~ a n d ~ } C _ { f } \mathrm { ~ i s ~ n o t } , } \\ { \displaystyle { \operatorname* { m i n } _ { b \in B _ { f } } \beta ( b , f ) } , } & { \mathrm { o t h e r w i s e } , } \end{array} \right.\tag{14}
$$

where $B _ { f }$ is the set of branches incident to the fork , $w ( c , f )$ is the significance of a concavity (Equation $( 7 ) , \omega ( \eta )$ ,is the salience of a link (Equation (3)) and K is an arbitrarily large constant that favours processing forks with assigned links before forks without a link, and forks with assigned concavities before forks without. Using the minimum branch salience terms $\beta ( b , f )$ generally favours a ,depth-first processing of forks. Figure 10 shows a typical sequence resulting from this ordering.

7.3.8 Updating H. As with half-junctions, we remove vertices (concavities) and edges (links) from H after each junction identification. We remove a concavity from H if it is shared by two previously processed links that are assigned to the same fork, and if it is the representative concavity of a Y-junction. Finally, every time we process a T-junction, we test if the good continuation along the link is greater than a relatively high threshold (0 4 in the examples given). If this is the case, then we remove both concavities from H. This is based on the observation that separating the protrusion identified by the representative link can produce a locally flat region in the neighborhood of the discarded concavities.

![](images/a01b38d9d4f5047e6152427a9186aac35b8a88160c91d65cb94e20db9234201f.jpg)  
Fig. 16. Faces and edges of Q for different junction types. The tangents determining the edges are marked in black. (a) A T-junction adds one edge and produces two faces, one including the two arc segments of the concavities’ contact regions. (c) A Y-junction adds one edge and produces two faces. (d) Three half-junctions in the same area, adding 12 edges (3 quadrilaterals).

## 7.4 Step 4: Convert T-junction Pairs to Half-junction

In certain configurations such as the one emphasized in Figure 15(a), an area that is characterized by two ligature regions is perceived to be coverd by two crossing strokes. However, the steps described so far result in identifying two T-junctions that produce two strokes incident to a common stroke (Figure 15(b)). We check if this kind of configuration can be transformed into one consisting of two crossing strokes (Figure 15(c)), with a procedure similar to the one used for half-junctions in Section 7.2. If the distance between the incident endpoints of the two strokes is less than both radii of the forks covered by the T-junctions, and the good continuation $\psi ( \eta _ { i } , \eta _ { j } )$ for the junction links is greater than ,the same threshold used in Section 7.2, then we construct one halfjunction from the two links and discard the two T-junctions. The result is similar to the one produced by two half-junctions, but in this case one half-junction connects two previously disconnected strokes, while one stroke has been already connected by the previously identified T-junction pair.

## 8 STROKE RECONSTRUCTION

The stroke graph S, together with junctions, provides a flexible, high-level descriptor of the inferred stroke structure of a font. We use this descriptor in two methods to reconstruct strokes. Our first method produces strokes using the traditional definition of a stroke—a spine paired with a varying width profile function. The second produces stroke areas, a type of part-decomposition of the glyph consisting of potentially overlapping shapes that when unified closely reproduce the original glyph.

## 8.1 Strokes

To recover a spine and a width profile function from a connected component of S we consider the concatenated sequence of stroke segments associated with each branch in the component. Each sequence is akin a polyline in $\mathbb { R } ^ { 3 }$ with each coordinate $[ { \pmb y } _ { i } , r _ { i } ]$ ,consisting of an adjusted position concatenated with an adjusted radius. To remove small discontinuities that can persist after the adjustment steps, we smooth the coordinates with a conventional spline method. We perform smoothing in a piecewise manner, with pieces delimited by the stroke endpoints and at L-junctions.

We also check for strokes that can be closely approximated with a straight spine and a constant width profile. To do so, we compute a linear least square fit of a 3D line to the coordinates and use this line if the mean-squared error of the fit is less than a userconfigurable threshold.

![](images/ca65fe7a712307be1e1954e49ab868b7ff622a18e4b731f537a2744ae79b08f3.jpg)  
Fig. 17. Stroke areas for the letter R in different fonts. The last result is based on a stroke that crosses itself, producing a stroke area with a hole.

## 8.2 Stroke Areas

A stroke area is a 2D part of the glyph derived from a single stroke. Stroke areas enable stylizations that depend on the shape of the stroke parts and help quantify the accuracy of our segmentations (Section 9.1). They are created by using junctions to partition the input shape into disjoint faces and then using the connected components of the stroke graph to guide the assembly of these faces into stroke areas.

We construct a planar map [Fabri and Pion 2009; Preparata and Shamos 1985] Q built from the glyph outline with additional edges derived from the junctions. Each T-junction adds one edge to Q, connecting the origins of tangents on the ends of its link (Figure 16(a)). Each Y-junction also adds one edge to Q.

We take the direction of one of the tangents of the junction’s representative concavity and connect the concavity extremum to the first intersection with the outline. The tangent is the one that is least aligned with the protruding branch (Figure 16(c)). A halfjunction adds a quadrilateral to the graph. Two of its edges connect the tangent origins of the non-crossing link endpoint pairs, the same ones used to compute good continuation in Section 7.2. The other two edges connect the same tangent origins along the links (Figure 16(d)).

Once Q has been constructed, we create one area for each stroke by performing a union of some of the faces in Q. We first construct a disk area for each stroke. Each area is the union of the disks for the branches in the associated connected component of S as well as for any branches discarded by a junction that covers a branch in this connected component. We then assign any face enclosed by any of the quadrilaterals added by a half-junction to the stroke for that half-junction. Each remaining face is assigned to the stroke for which the intersection of the face and the stroke disk area is largest. Figure 17 shows the stroke areas for the letter R in various fonts.

## 9 RESULTS AND DISCUSSION

Strokes and stroke areas provide the basis for evaluating our method with respect to ground-truth segmentations and for producing a variety of stroke-based stylizations of the input glyphs.

## 9.1 Segmentation Quality

Quantitative evaluation of the results of stroke segmentation is difficult, because there is no ground truth for most Western fonts. However, we can compare the segmentation results with the makeme-a-hanzi dataset [Kishore 2018], which includes outline and stroke ground truth for a variety of simplified and traditional Chinese (Han) characters. To perform the evaluation, we first segment the glyph into stroke areas as described in the previous section.

![](images/d5f9edfe56fc9d1702c0fe6c75de7813290c577c247d8f94f892d01790e7f762.jpg)  
Fig. 18. Quantitative evaluation with the make-me-a-hanzi dataset; the ground truth is to the right of each pair. (a) Our method derives the same stroke structure as that of the ground truth but one T-junction (marked with a red circle) includes a stroke deformation. (b) All strokes are correctly identified by our method except for the middle area, emphasized in red. We derive one single stroke rather than the two in the ground truth, because there is no salient concavity near the top left of that area. (c) Using $\lambda _ { \gamma } = 1$ for L-junctions results in a segmentation different from the .ground truth. With an increased value of $\lambda _ { \gamma } = 1 . 2$ the segmentation is .identical to the ground truth, globally producing the results discussed in Section 9.1.

Similarly to Kim et al. [2018], we then perform an Intersection over Union (IoU) test on the rasterized stroke areas. For each segmented stroke area, we identify the most similar stroke from ground truth by maximizing the intersection area. Rasterizing at a resolution of 512 × 512 gives an average per pixel accuracy of 0 979, which is slightly better then the result of 0 958 reported by . .Kim et al. [2018]. This result is influenced by some inaccuracies in the planar map edges (Figure 18(a)) and by different stroke decompositions (Figure 18(b)). We consider a stroke to be incorrect if its IoU is 0.8, which excludes small errors like the one in Figure 18(a), and results in a per-stroke accuracy of 0 976.

.Certain ground-truth decompositions cannot be deduced from the outline alone, because they depend on domain knowledge. For example, “boxes” in Chinese characters should almost always be segmented into three strokes. Sometimes there are outline details that lead to a correct segmentation, but not always (Figure 18(b)). In other cases, the segmentation result is sensitive to parameter choices. For example, with the parameters used throughout the article for Western fonts, Figure 18(c) results in a corner being interpreted as a Y-junction. For the make-me-a-hanzi dataset we found that using a value of $\lambda _ { \gamma } = 1 . 2$ for L-junctions (Section 7.3.6) .fixed cases like Figure 18(c) and generally improved the segmentation results. With this parameter choice only 8% of the glyphs in the make-me-a-hanzi dataset had segmentation errors that were not of the types discussed above; 11% had errors that could not be avoided without domain knowledge or different parameter choices, and 81% were segmented identically to the ground truth. From a qualitative viewpoint, 100% of our segmentations produced strokes that create a readable reconstruction and robust stylization of the glyph, independent of the choice of parameters.

We further tested our method on 100 fonts and it generates plausible segmentation results in the vast majority of cases. The most encountered failure case is for very thick glyphs in which the average stroke thickness is larger than the average stroke length (Figure 19), leading to a medial axis with branches that cannot readily be discarded as non-salient. The segmentation also gives useful results on other types of non-glyph shapes as long as there is a recoverable articulated or branching structure (Figure 20). This suggests that our method could be useful to recover stroked paths from filled vector art or from scanned documents.

![](images/7c810f0e09f86cc305efad177c514c6cda726903f7fc93075b376cb91da463e7.jpg)  
Fig. 19. Challenging case with a glyph in the Manicotti font. The first row shows the character “A,” which produces non-salient features similar to stroke ends that are, in (a), nested within the branching structure of the medial axis, in (a), do not produce a medial axis subtree that our method is able to identify as a stroke-end junction. These cases are difficult to detect with our current junction taxonomy and result, in (b), in an inplausible stroke decomposition, and, in (c), in an area decomposition that simply ignores the non-salient features. In the second row the ends of the top and bottom serifs have been slightly extended, disambiguating the medial axis and giving plausible strokes and areas.

![](images/7c868542060fc8f6a3db16981deb5448f56ec27ead7091eb90b583ce40db224d.jpg)  
Fig. 20. Stroke decomposition of silhouettes. The left mammal silhouette (from the PhyloPic database, http://phylopic.org) results in strokes that capture its articulated structure. The right hand results in a plausible reconstruction, but the segmentation deviates from the perceived structure of a hand, with the pinkie being part of the same “stroke” as the palm.

## 9.2 Stylization and Animation

Strokes and junctions provide the basis for a variety of stylization methods. In particular, junctions provide semantic annotations that determine connectivity relations between strokes or features such as corners that can be preserved across stylizations. Grounding text stylization on fonts has a number of advantages: (i) the large variety of existing fonts provides a large variety of starting points for stylization, (ii) the method is agnostic to the language or writing system, and (iii) the embedded kerning information can be used to determine inter-glyph spacing, which is known to be difficult to achieve with methods that create stylized text from scratch [Haines et al. 2016].

9.2.1 Skeletal Strokes. The spines recovered from the stroke graph can be directly used to produce some simple stylizations. Fitting Bézier curves to each spine can produce “Hershey fonts,” which have glyphs consisting of constant-width strokes (Figure 21). Such fonts are well suited for fabrication and manufacturing applications. The same curves can be used as the spines for skeletal

#

Fig. 21. Hershey font stylization (black) overlayed on the original font (gray).

![](images/90acd963b3943729f993e487c532f87e6bf376bbe8c01c945e79d3ddd98358a0.jpg)

Fig. 22. Font stylization with skeletal strokes. The left column shows the text in the original font. The right column shows the corresponding stroke stylizations. The first example on the right shows the result of using skeletal strokes as implemented in Adobe Illustrator to change weight, cap, and join styles; the other three show various decorative effects. The strokes in the bottom right example use variable width.

![](images/5cb5e95603aff6f18e1b9dee3d6101ffa6ca14f2c567e900e7008325fdbe81f3.jpg)  
Fig. 23. Simplification and schematization of the strokes in Figure 21: (a) Path simplification. Spine schematization [Dwyer et al. 2008]: (b) quantizing orientations to multiples of 60◦; (c) restricting orientations to 30◦ and 120◦.

strokes [Hsu and Lee 1994], which enable a variety of glyph stylizations ranging from painterly to decorative (Figure 22).

9.2.2 Schematization. We can also generate stylizations by simplifying the spines into sparse control polygons and schematizing the results. This can be done with a number of polygonal simplification methods; we use Discrete Contour Evolution [Latecki and Lakämper 1998] with a user-controlled threshold (Figure 23). For a schematized stylization, we quantize the orientations of stroke segments using the C-oriented method [Nöllenburg 2014], which approximates a polyline with another one consisting of segments having a discrete set of orientations. We use the solution of Dwyer et al. [2008], which creates regular-looking polygonizations and stylistic abstractions of the letter structure (Figure 23(b) and (c)). These also form the basis for other stylization techniques described below.

Structural adjustment. Schematization applies to each stroke separately. This can corrupt the glyph topology by disconnecting strokes that previously met at T- or Y-junctions. However, the connectivity information encoded by these junctions allows us to

![](images/a87a1c141977faeb3b04928c011beffc2526135bf44a5f543e727f2269954c38.jpg)

ABRACADABRA

![](images/694bbdb0fed108b6a2a012f4b32c9127642f0cd5933b23f6bc0d93b43b16a5cd.jpg)

![](images/a909a43876a0aa0a4bd898a44ddcc48b6c8a0cc7cffce59afa6f6f3226d1e1d1.jpg)

Fig. 24. Schematization and smoothing applied to strings in different fonts (Apollo ASM, Impact, Amador). The second example in (c) shows stroke ends extended for calligraphic effect. The second example in (a) and both examples in (c) use varying brush thickness derived from the stroke width profiles

correct these errors by extending spines along their end-tangents until they intersect their opposite nearby spine. We use a similar procedure to maintain structural relations between strokes in the stylization methods that follow, with details given in Appendix C.

9.2.3 Calligraphic Effects. The schematized or simplified vertices of a spine can be used as a motor plan for generating motion paths that mimic the aesthetics of certain kinds of calligraphic writing (Figures 1(e) and (f) and 24). We generate smooth trajectories with the adaptive smoothing method of Berio et al. [2017] and increase dynamism by varying brush thickness depending on the synthesized trajectory speed [Berio et al. 2018], or depending on the width profile of a stroke (Figure 24), similarly to Seah et al. [2005]). Different degrees of smoothing at the corners results in different calligraphic effects.

9.2.4 Graffiti Art. The origins of graffiti styles can be traced back to more traditional forms of calligraphy and lettering as well as to certain types of fonts [Arte 2015]. We can simulate this contemporary art form, which features disctinctive forms of letterstylization, with a variant of skeletal strokes [Berio et al. 2019] that mimics the intertwining, folding and extrusion effects that can be seen in traditional graffiti art (Figure 25). The local width of each stroke can be determined by the previously computed thickness profile, and multiple strokes optionally can be combined with local union operations at T- and Y- junctions and half-junctions. We also use curve smoothing [Berio et al. 2017] and the rendering methods of Berio et al. [2019] to provide smooth color gradations, solid-colored blocks, and highlight effects common to contemporary graffiti (Figure 26).

![](images/a2a655d1eb78f547c5f20cd1d1f99235c745fb65248d6c62b9e8e8578a7ccfdc.jpg)  
Fig. 25. Schematization and “graffiti strokes” [Berio et al. 2018] applied with the same parameters to the letter “A” in different fonts (Andes, Giddyup, Doctor Fibes, College, Apollo ASM). In the last two examples (bottom left), the serifs are replaced with arrow heads.

![](images/e47dcbb320cf2cdc011d32968ad2c9772d4d5695d2d80040ecf31f4ab5492109.jpg)  
Fig. 26. Mimicking graffiti effects with the layering and rendering techniques of Berio et al. [2018].

9.2.5 Structural Modifiers. T-, Y-, and L-junctions identify strokes that can be altered for additional stylization effects. Strokes that do not terminate in one of these junctions can be extended to achieve various visual effects (Figure 24, last row). Junctions also help identify serifs. We detect a serif as a relatively short, straight stroke that contains the connected portions of one single T-junction and does not contain any other Y- or L-junction. This detection can be exploited for stylization, for example, replacing serifs with arrow heads as is common in graffiti (Figure 25).

![](images/37c3e579c37da378fd79ca8dfe48f473e33ac98768a4791b411b7432f7dcedcb.jpg)  
Fig. 27. Animating the drawing of a stylized R.

![](images/edda62b714d41fabe3acb011c63a1c97bd001e6996bbbf6db6a188ad89666af3.jpg)

Fig. 28. Stylization based on similarity between stroke areas. In the first row, strokes are color-coded based on common clusters. In the second row, each stroke in a cluster is replaced with the same custom artwork. Note that including junction structure in the stroke similarity metric allows distinct stylizations to apply to otherwise-similar strokes, like the horizontal strokes in R, P, L, and A. Artwork ©Daichi Ito, Adobe Research. The same stroke areas can be used to drive other replacement-based stylization methods such as the one by Zhang et al. [2017].

9.2.6 Stroke Animation. Strokes can be used as motion paths to generate a variety of animation effects. The smoothing method of Berio et al. [2017] produces dense polylines, with distances between vertices reflecting the kinematics that are similar to human hand motion. This can be exploited to generate natural-looking stroke animations (Figure 27). Stylized brush animations can also be generated by incrementally visualizing a stroke, or by animating a particle system that follows the stroke’s path. We order strokes with a simple topological sorting heuristic rewarding topto-bottom and left-to-right movements, but the strokes derived by our method are suitable for more sophisticated approaches [Fu et al. 2011; Tang et al. 2017].

9.2.7 Area-based Stylization: Stroke Similarity. The same stroke areas used to evaluate segmentation are also the basis of a similarity measure among strokes in a complete font. We compute the difference between two stroke areas by aligning their centroids, rasterizing them, and then measuring the Jaccard distance [Deza and Deza 2013, p. 299] between the resulting bitmaps: 1 minus the intersection divided by the union. If one stroke terminates in a Tor Y-junction and the other does not, then the distance takes the maximum value of 1. We then group strokes using single-linkage agglomerative clustering and determine clusters based on a userconfigurable threshold. While the distance is computed offline, the clustering procedure is interactive, and users can adjust the threshold to their preference. We then replace each stroke area in a cluster with an artistic rendering based on the shape, generating stylizations that apply uniformly across an entire font (Figures 1(i) and 28).

## 9.3 Implementation Details

The core segmentation procedure is written in the Python programming language, and includes the QHull library [Barber and Huhdanpaa 1995] to efficiently compute 2D Voronoi diagrams used for medial axes recovery. We executed our methods on a 2.7-GHz Intel Core i7 processor with four cores. Outline analysis and segmentation together take an average of 2 seconds per glyph; normally we precompute these for an entire font, but they could also be computed on demand and cached. The stylization procedures described in this section are written in C++ using OpenGL for hardware-accelerated rendering. They run in real-time and allow exploring different stylizations through an interactive user interface.

## 10 CONCLUSION

In this article we first presented concepts and algorithms to automatically segment font glyphs into strokes, and then demonstrated how such strokes can be used to generate in real time a variety of stylizations of the input. We introduced along the way a number of innovations, namely:

(1) Using CSFs that describe convex and concave outline regions. (2) Links that connect concave CSFs across the body of a glyph and describe potential stroke crossings.

(3) A set of seven junction types—half-, T-, Y-, L-, stroke end, protuberance, and null—that characterize MI sub-structures and determine semantic stroke attributes useful to drive structurally-aware stylizations of a glyph.

(4) A novel application of association fields [Ernst et al. 2012] to the problem of stroke segmentation of glyphs.

Our system, StrokeStyles, solves a long-standing inverse problem of segmenting 2D font glyphs [Wang 2013, Section 4]. The strokes we can recover are based on spines and profile functions and enable a variety of stylization methods including skeletal strokes [Hsu et al. 1993], animation, calligraphy, and graffiti.

In this article we did not compare our stylizations with the ones produced by existing methods, because our objective of producing stylization based upon the glyph structure is entirely new. Our real-time stylization framework provides a “sandbox” in which a user/designer can explore many different options, ranging from readable stylizations to highly abstract renditions that still evoke the original font structure. This especially applies to the calligraphic and graffiti stylzations, which can operate in a domain where aesthetics take priority over readability [Craveiro 2017].

Stroke segmentation can also be useful in related applications like automatic font hinting [Shamir 2003], segmenting characters in historical documents [Lamiroy et al. 2015], painterly applications of robotic [Deussen et al. 2012], stylization methods that require taking glyph structure into account [Zou et al. 2016], animated reconstructions of arbitrary glyphs [Gingold et al. 2008] and producing training data for sequence-based generative models [Ha and Eck 2018; Kotani et al. 2020].

Data-driven approaches based on deep-learning typically rely on a large body of human-labelled training data. We instead demonstrate a solution that relies on experimentally validated principles of visual perception and computational geometry concepts. The advantage of our approach is that it is adaptable to fonts for which training data might be scarce or non-existent and to glyphs that do not match the training data. Our solution requires tuning a few parameters, but these have intuitive visual and perceptual interpretations and can be adjusted by the user for the required use case.In Section 9.1 for example, we have adjusted the system parameters to increase segmentation accuracy for Han characters. Such parameter changes could also be determined depending on information encoded as font metadata.

In future research, we plan to explore how data-driven solutions could be combined with our approach. For example, we could use data to incorporate language-specific domain knowledge. More specifically, we could add a data-driven term to Equation (11) to help identify junctions while still using the geometric and perceptual factors that we have defined. In our experiments we also have considered using measures such as stroke-radius variation or quality of fit to concave glyph areas. We finally selected the measures described in Section 7.3 as a sufficient minimum to produce plausible stroke segmentation for the glyphs we tested.

## APPENDICES

## A CSF COMPUTATIONS

When searching for additional CSFs (Section 4.2.1), we need to avoid false positives, particularly those associated with outline segments that approximate spirals. A spiral is a curve segment with monotonically-varying curvature. Such a curve does not have any curvature extrema between its ends [Leyton 1987] and thus should not produce an additional CSF. This can be further characterized by the Tait-Kneser theorem [Ghys et al. 2013], which states that all osculating circles of a spiral segment with strictly positive or negative curvature are disjoint and nested. However, because CSF analysis operates on a sampled curve, looking for additional CSFs for an outline segment that closely resembles a spiral is likely to produce many additional terminal branches and spurious CSFs (Figure 29(a), (b)). To avoid such false positives, we compute the degree of overlap δC ∈ [0 1] between any two discs as the area ,of their intersection divided by the area of the smaller disk. We then discard any new terminal disk if there is a pre-existing CSF with a smaller disk radius and for which the degree of overlap is greater than a user-defined threshold, which we empirically set to 0 98 (Figure 29(c)).

Once we have identified the CSFs for a given outline, we compute a pair of tangents for each concave CSF (Section 4.2.2). To evaluate the tangents, we compute a tangent cover along each support segment, from which we keep the first tangents next to the ends of the contact region. We use “sleeve fitting” [Zhao and Saalfeld 1997] for this purpose. The more recent “alpha thick segments” technique [Faure et al. 2009] could also be used.

## B ASSOCIATION FIELDS

Our association fields are adapted from Ernst et al. [2012]. The model predicts the conditional link probability of one oriented element relative to another. The link probability α is given by the product $A ^ { \phi } A ^ { d }$ of an angular and a radial component. The angular component parameterizes deviations from perfect cocircularity and deviations from zero curvature with the product of two von Mises distributions, analogs of Gaussian distributions with a circular support. Given two orientations $\phi _ { i } , \phi _ { j }$ and planar positions $( x _ { i } , y _ { i } ) , ( x _ { j } , y _ { j } )$ ,the angular component simplifies to

![](images/e35fe1a49888010804a00ecc595ac32ca2eca2140265eaf1f0a8b125af95ed5e.jpg)  
Fig. 29. Overlapping disks along a spiral segment. (a) the segment in red between the contact regions of the two CSFs is a spiral. However its local medial axis has two branches producing two terminal disks, shown in gray. (b) Without filtering, the left disk produces an additional CSF, since it is slightly more salient than the other disk. (c) However, the disk fully encloses the previously identified one so it is discarded. This results in the spiral segment not producing any new CSF.

$$
A ^ { \phi } = \frac { C } { 4 } \cosh { \left( \frac { 1 } { \sigma _ { \beta } ^ { 2 } } \cos { ( \beta / 2 ) } + \frac { 1 } { \sigma _ { \theta } ^ { 2 } } \cos { ( \theta - \beta / 2 ) } \right) } ,\tag{15}
$$

with $\beta ~ = ~ \phi _ { j } ~ - ~ \phi _ { j } , ~ \theta ~ = ~ \tan ^ { - 1 } \left( \left( y _ { j } - y _ { i } \right) / \left( x _ { j } - x _ { i } \right) \right) ~ - ~ \phi _ { i }$ , and $\sigma _ { \theta } ~ = ~ 0 . 2 7$ and $\sigma _ { \beta } ~ = ~ 0 . 4 7$ the spread parameters for cocircularity and curvature.3 We use the spread parameter values that were experimentally found to be optimal by Ernst et al. [2012]. The constant C is a normalization factor derived from the von Mises distribution, with:

$$
C = \pi ^ { 2 } I _ { 0 } \left( 1 / \sigma _ { a } ^ { 2 } \right) I _ { 0 } \left( 1 / \sigma _ { b } ^ { 2 } \right) ,\tag{16}
$$

where $I _ { 0 }$ is the modified-Bessel function of the first kind with order 0. We also divide $A ^ { \phi }$ by 0 602, so it falls in the [0 1] range, . ,which facilitates parameter setting in our application-driven use case.

For the task of grouping closely-spaced oriented elements, Ernst et al. [2012] express the radial component as an exponential function that decays with distance. Again, we opt for a formulation that facilitates parameter tuning and express the component with a Gaussian decay:

$$
A ^ { d } = \exp \Big ( d ^ { 2 } / \Big ( 2 \sigma _ { d } ^ { 2 } \Big ) \Big ) ,\tag{17}
$$

with d the distance between the two positions and $\sigma _ { d }$ a distancespread. We set $\sigma _ { d }$ to twice the maximum $\mathbb { M } _ { + } ^ { I }$ radius when computing good continuation for links (Section 7.2), and to the distance between the tangent origins when computing tangent origins during Y-junction interpretation (Section 7.3.2).

## C STRUCTURAL ADJUSTMENTS

The schematization and smoothing procedures discussed in Section 9.2 modify stroke geometry, which can corrupt the structural relations between strokes. However, junctions provide the necessary information for rectifying these relations.

Schematization adjustment. Schematization [Dwyer et al. 2008] is applied to each stroke separately. This can corrupt the topology of stylized glyph, making it difficult to apply intersection-based adjustments to the stroke endpoints. While a correct topology could be imposed with constraint solving algorithms [Nöllenburg 2014], we observe that this issue mostly affects strokes such as the lower-left serif in Figure 30(b), which has another stroke ending within it. This configuration can be detected by counting the number of T-junctions and branching Y-junctions along a stroke. If, for a given stroke, only one such junction exists, then we translate the stroke by ${ \pmb { p } } ^ { \prime } - { \pmb { p } } ,$ where p is the original endpoint of the incident stroke and $\pmb { p } ^ { \prime }$ is the endpoint after schematization (Figure 30(c)). After executing this procedure, we can shift the stroke endpoints to the closest intersection of the end-tangents with the opposite stroke (Figure 30(d)).

![](images/73dda0ab75fcaf2eb982fce097e15954d9ba7af55898f3c57f93215d55cb31c1.jpg)  
Fig. 30. Structural adjustment steps for a stylized letter “A”. (a) Unstylized stroke spines after segmentation. (b) Schematization can corrupt topological relations among strokes. (c) We reestablish these by shifting strokes that are covered by a single T-junction or branching Y-junction. Note that the triangular part of the $^ { * } { \cal A } ^ { * }$ is covered by two T-junctions, so it is not adjusted. (d) A second adjustment step reconnects all stroke endpoints. (e) Using the schematized stroke as a control polygon for a smoothing method can also corrupt the incidence relations among strokes. (f ) A last adjustment step moves the non-smoothed polygon endpoints (the middle section of the “A”) so they terminate at the intersection with the smoothed strokes.

Smoothed stroke adjustment. Smoothing also can corrupt the adjacency relations between strokes. This is especially likely to occur when using a simplified or schematized spine as an input for a stylized smoothing method such as the one by Berio et al. [2017] (Figure 30(e)). To adjust these configurations, we perform a first smoothing pass on each stroke. We then adjust the endvertices of the spines used as an input to the smoothing methods, so that the non-smoothed spines are incident to the smoothed ones (Figure 30(f )).

## D LIST OF SYMBOLS

x Outline point – Section 4.1   
f Fork (degree-3 medial axis vertex) – Section 4.1   
t Tangent – Section 4.2.2   
n Inward normal at CSF – Section 4.2.2   
$x _ { c }$ CSF extremum – Section 4.2   
$_ { { \pmb y } }$ Medial axis point – Section 4.1   
$\varphi _ { i , j }$ Flow of a link for the concavity pair (ci , cj ) – Section 5.1   
$\pi$ Protruding direction of a branch – Section 5.1   
$\pmb { \mathscr { P } }$ Scalar product of $\varphi _ { i , j }$ and π Section 5.1   
$F$ ,A set of forks – Section 6   
$r$ Disk radius of medial axis vertex – Section 4.4.1   
${ \pmb y } _ { f }$ Fork’s position – Section 7.3.3   
$r _ { f }$ Fork disk radius – Section 7.3.3   
$\bar { d _ { f } } , d _ { e }$ Radius-weighted distances – Section 4.4.1   
$s _ { f _ { \mathrm { m a x } } }$ Max geodesic length from a fork along MI – Section 4.4.1   
$\sigma _ { d }$ Spread parameter for ψ – Sections 5.3 and B   
b Medial axis branch – Section 4.1   
c CSF – Section 4.2

η C Link – Section 5   
$\gamma$ Junction – Section 6   
$H$ A set of valid links (also H ) – Section 7   
$j _ { f }$ Set of candidate junctions of a fork –   
Section 7.3.5   
B A set of branches – Section 7.3.7

## Objects/Structures

MI Interior medial axis – Section 4.1   
$\mathbb { M } ^ { E }$ Exterior medial axis – Section 4.1   
S Stroke graph – Section 6.2   
$\mathbb { H }$ Graph of valid links and concavities - Section 7   
$\mathbb { Q }$ Planar map used to construct stroke areas –   
Section 8.2

## Saliency/significance measures

$\beta ( b , f )$ Salience of branch b protruding from fork f – Section 4.1.2

$\omega ( \eta )$ Link salience – Section 5.2

ψ Good continuation – Sections 5.2, 5.3 and B

$\Lambda$ Junction evaluation measure – Section 7.3

$w ( c , f )$ Significance of a concavity with respect to a fork f – Section 7.3.3

$\Lambda _ { \mathbb { I } }$ Measure of coverage – Sections 7.3 and 7.3.1

$\Lambda _ { \psi }$ Measure of smoothness – Sections 7.3 and 7.3.2

$\Lambda _ { w }$ Measure of concavity significance – Sections 7.3 and 7.3.3

$\Lambda _ { \eta }$ Measure of link salience – Section 7.3

## Thresholds and Tolerances

τ β Branch saliency threshold – Section 4.1.2

$ { { \beta } } _ { \mathrm { m i n } }$ Branch saliency lower bound – Section 7.3.5

$\lambda _ { \mathrm { L } }$ Maximum concavity radius multiplier for

$r _ { h }$ Maximum CSF radius, divided by glyph height Section 4.2.1

## REFERENCES

Ery Arias-Castro, Gilad Lerman, and Teng Zhang. 2017. Spectral clustering based on local PCA. J. Mach. Learn. Res. 18, 1 (2017), 253–309.

Anssi Arte. 2015. Forms of Rockin’: Graffiti Letters and Popular Culture. Dokument Press.

Jonas August, Kaleem Siddiqi, and Steven W. Zucker. 1999. Ligature instabilities in the perceptual organization of shape. Comput. Vis. Image Understand. 76, 3 (1999), 231–243. https://doi.org/10.1006/cviu.1999.0802

Samaneh Azadi, Matthew Fisher, Vladimir G. Kim, Zhaowen Wang, Eli Shechtman, and Trevor Darrell. 2018. Multi-content GAN for few-shot font style transfer. In Proceedings of the IEEE Conference on Computer Vision and Pattern Recognition. 7564–7573. https://doi.org/10.1109/CVPR.2018.00789

Alex Bailey. 2001. Class-dependent Features and Multicategory Classification. Ph. D. Dissertation. Southampton University.

Elena Balashova, Amit H. Bermano, Vladimir G. Kim, Stephen DiVerdi, Aaron Hertzmann, and Thomas Funkhouser. 2019. Learning a stroke-based representation for fonts. Comput. Graph. Forum 38, 1 (2019), 429–442. https://doi.org/10. 1111/cgf.13540

Brad Barber and H. Huhdanpaa. 1995. QHull. The Geometry Center, University of Minnesota.

Alexander Belyaev and Shin Yoshizawa. 2001. On evolute cusps and skeleton bifurcations. In Proceedings of the International Conference on Shape Modeling and Applications. IEEE, 134–140. https://doi.org/10.1109/SMA.2001.923384

Daniel Berio, Paul Asente, Jose Echevarria, and Frederic Fol Leymarie. 2019. Sketching and layering graffiti primitives. In Proceedings of the 8th ACM/Eurographics Expressive Symposium on Computational Aesthetics and Sketch Based Interfaces and Modeling and Non-Photorealistic Animation and Rendering. 51–59. https://doi. org/10.2312/exp.20191076

Daniel Berio, Sylvain Calinon, and Frederic Fol Leymarie. 2017. Dynamic graffiti stylisation with stochastic optimal control. In Proceedings of the 4th International Conference on Movement Computing. Association for Computing Machinery. https://doi.org/10.1145/3077981.3078044 Article no. 18.

Daniel Berio, Frederic Fol Leymarie, and Réjean Plamondon. 2018. Expressive curve editing with the sigma lognormal model. In Proceedings of the 39th Annual European Association for Computer Graphics Conference: Short Papers. Eurographics Association, 33–36.

Daniel Berio, Frederic Fol Leymarie, and Réjean Plamondon. 2020. Kinematics reconstruction of static calligraphic traces from curvilinear shape features. In Proceedings of the Lognormality Principle and its Applications in e-Security, e-Learning and e-Health, Réjean Plamondon, Angelo Marcelli, and Miguel Ángel Ferrer (Eds.). Series in Machine Perception and Artificial Intelligence, Vol. 88. Chapter 11, 237–268. https://doi.org/10.1142/9789811226830\_0011

Harry Blum. 1973. Biological shape and visual science (part I). J. Theor. Biol. 38, 2 (1973), 205–287. https://doi.org/10.1016/0022-5193(73)90175-6

Joseph L. Brooks. 2015. Traditional and new principles of perceptual grouping. In The Oxford Handbook of Perceptual Organization, Johan Wagemans (Ed.). Oxford University Press, 57–87.

Neill D. F. Campbell and Jan Kautz. 2014. Learning a manifold of fonts. ACM Trans. Graph. 33, 4 (2014). https://doi.org/10.1145/2601097.2601212 Article no. 91.

Xudong Chen, Zhouhui Lian, Yingmin Tang, and Jianguo Xiao. 2017. An automatic stroke extraction method using manifold learning. In Proceedings of the European Association for Computer Graphics: Short Papers (EG’17). Eurographics Association, 65–68. DOI:10.2312/egsh.20171016

Charles H. Cox, Philippe Coueignoux, Barry Blesser, and Murray Eden. 1982. Skeletons: A link between theoretical and physical letter descriptions. Pattern Recogn. 15, 1 (1982), 11–22. https://doi.org/10.1016/0031-3203(82)90056-5

Rodrigo Pena Carvalho Dos Anjos Craveiro. 2017. The influence of graffiti writing in contemporary typography. Street Art Urban Creativ. Sci. J. 3, 2 (2017), 65–83. https://doi.org/10.25765/sauc.v3i2.82

Joeri De Winter and Johan Wagemans. 2006. Segmentation of object outlines into parts: A large-scale integrative study. Cognition 99, 3 (2006), 275–325. https://doi. org/10.1016/j.cognition.2005.03.004

Oliver Deussen, Thomas Lindemeier, Sören Pirk, and Mark Tautzenberger. 2012. Feedback-guided stroke placement for a painting machine. In Proceedings of the 8th Annual Symposium on Computational Aesthetics in Graphics, Visualization, and Imaging. Eurographics Association, 25–33.

Shay Deutsch and Gérard Medioni. 2017. Learning the geometric structure of manifolds with singularities using the tensor voting graph. J. Math. Imag. Vis. 57, 3 (2017), 402–422. https://doi.org/10.1007/s10851-016-0684-2

Michel Marie Deza and Elena Deza. 2013. Encyclopedia of Distances. Springer. https: //doi.org/10.1007/978-3-642-30958-8

Tim Dwyer, Nathan Hurst, and Damian Merrick. 2008. A fast and simple heuristic for metro map path simplification. In Proceedings of the International Symposium on Visual Computing. Springer, 22–30. https://doi.org/10.1007/978-3-540-89646- 3\_3

Udo A. Ernst, Sunita Mandon, Nadja Schinkel–Bielefeld, Simon D. Neitzel, Andreas K. Kreiter, and Klaus R. Pawelzik. 2012. Optimality of human contour integration. PLOS Comput. Biol. 8, 5 (2012), 1–17. https://doi.org/10.1371/journal.pcbi.1002520

Andreas Fabri and Sylvain Pion. 2009. CGAL: The computational geometry algorithms library. In Proceedings of the 17th ACM SIGSPATIAL International Conference on Advances in Geographic Information Systems (GIS’09). 538–539. https: //doi.org/10.1145/1653771.1653865

Alexandre Faure, Lilian Buzer, and Fabien Feschet. 2009. Tangential cover for thick digital curves. Pattern Recogn. 42, 10 (2009), 2279–2287. https://doi.org/10.1016/j. patcog.2008.11.009

Jean-Dominique Favreau, Florent Lafarge, and Adrien Bousseau. 2016. Fidelity vs. simplicity: A global approach to line drawing vectorization. ACM Trans. Graph. 35, 4 (2016). https://doi.org/10.1145/2897824.2925946 Article no. 120.

Vicky Froyen, Jacob Feldman, and Manish Singh. 2015. Bayesian hierarchical grouping: Perceptual grouping as mixture estimation. Psychol. Rev. 122, 4 (2015), 575– 597. https://doi.org/10.1037/a0039540

Hongbo Fu, Shizhe Zhou, Ligang Liu, and Niloy J Mitra. 2011. Animated construction of line drawings. In ACM Trans. Graph. 30 (2011). 1–10. https://doi.org/10.1145/ 2070781.2024167

Mikel Galar, Alberto Fernández, Edurne Barrenechea, Humberto Bustince, and Francisco Herrera. 2011. An overview of ensemble methods for binary classifiers in multi-class problems: Experimental study on one-vs-one and one-vs-all schemes. Pattern Recogn. 44, 8 (2011), 1761–1776. https://doi.org/10.1016/j.patcog. 2011.01.017

Étienne Ghys, Sergei Tabachnikov, and Vladlen Timorin. 2013. Osculating curves: Around the tait-kneser theorem. Math. Intell. 35, 1 (2013), 61–66. https://doi.org/ 10.1007/s00283-012-9336-6

Peter J. Giblin and Benjamin B. Kimia. 2003. On the local form and transitions of symmetry sets, medial axes, and shocks. Int. J. Comput. Vis. 54, 1 (Aug. 2003), 143–157. https://doi.org/10.1109/ICCV.1999.791246

Yotam Gingold, David Salesin, and Denis Zorin. 2008. Stroke-by-Stroke Glyph Animation. Technical Report. Creativity and Graphics Lab (CraGL) at George Mason University, Fairfax, Virginia.

Andrew Goldberg, Xiaojin Zhu, Aarti Singh, Zhiting Xu, and Robert Nowak. 2009. Multi-manifold semi-supervised learning. In Proceedings of the 12th International Conference on Artificial Intelligence and Statistics, David van Dyk and Max Welling (Eds.), Vol. 5. PMLR, 169–176. https://proceedings.mlr.press/v5/goldberg09a.html.

David Ha and Douglas Eck. 2018. A neural representation of sketch drawings. In Proceedings o f the 6th International Conference on Learning Representations (ICLR’18).

Tom S. F. Haines, Oisin Mac Aodha, and Gabriel J. Brostow. 2016. My text in your handwriting. ACM Trans. Graph. 35, 3 (2016). https://doi.org/10.1145/2886099 Article no. 26.

Katherine A. Heller and Zoubin Ghahramani. 2005. Bayesian hierarchical clustering. In Proceedings of the 22nd International Conference on Machine learning (ICML’05). ACM, 297–304. https://doi.org/10.1145/1102351.1102389

Jacky Herz, Roger D. Hersch, and Jakob Gonczarowski. 1997. Coherent processing of character skeletal forms. Comput. Graph. 21, 6 (1997), 727–736. https://doi.org/10. 1016/S0097-8493(97)00050-2

Donald D. Hoffman and Whitman A. Richards. 1984. Parts of recognition. Cognition 18, 1-3 (1984), 65–96. https://doi.org/10.1016/0010-0277(84)90022-2

Donald D. Hoffman and Manish Singh. 1997. Salience of visual parts. Cognition 63, 1 (1997), 29–78. https://doi.org/10.1016/S0010-0277(96)00791-3

Douglas R. Hofstadter. 1982. Variations on a theme as the essence of imagination. Sci. Am. 247, 4 (1982), 14–21.

Siu Chi Hsu and Irene H. H. Lee. 1994. Drawing and animation using skeletal strokes. In Proceedings of the 21st Annual Conference on Computer Graphics and Interactive Techniques (SIGGRAPH’94), 109–118. https://doi.org/10.1145/192161.192186

S. C. Hsu, I. H. H. Lee, and N. E. Wiseman. 1993. Skeletal strokes. In Proceedings of the 6th Annual ACM Symposium on User Interface Software and Technology (UIST’93). 197–206. https://doi.org/10.1145/168642.168662

Changyuan Hu and Roger D. Hersch. 2001. Parameterizable fonts based on shape components. IEEE Comput. Graph. Appl. 21, 3 (2001), 70–85. https://doi.org/10. 1109/38.920629

Elena J. Jakubiak, Ronald N. Perry, and Sarah F. Frisken. 2006. An improved representation for stroke-based fonts. In ACM SIGGRAPH 2006 Sketches. https://doi.org/10. 1145/1179849.1180020

Tingting Jiang, Zhongqian Dong, Chang Ma, and Yizhou Wang. 2013. Toward perception-based shape decomposition. In Proceedings of the Asia Conference on-Computer Vision (ACCV’12). Lecture Notes in Computer Science, Vol. LNCS 7725. Springer, 188–201. https://doi.org/10.1007/978-3-642-37444-9\_15

Mark Kachanov, Boris Shafiro, and Igor Tsukrov. 2003. Handbook of Elasticity Solutions. Springer Netherlands. https://doi.org/10.1007/978-94-017-0169-3

Peter Karow. 1994. Digital Typefaces: Description and Formats. Springer. https://doi. org/10.1007/978-3-642-78105-6

Byungsoo Kim, Oliver Wang, A Cengiz Öztireli, and Markus Gross. 2018. Semantic segmentation for line drawing vectorization using neural networks. Comput. Graph. Forum 37, 2 (2018), 329–338. https://doi.org/10.1111/cgf.13365

Shaunak Kishore. 2018. Make Me a Hanzi Dataset. Retrieved from https://github.com/ skishore/makemeahanzi.

Donald E. Knuth. 1979. Mathematical typography. Bull. Am. Math. Soc. 1, 2 (1979), 337–373. https://doi.org/10.1090/S0273-0979-1979-14598-1

Atsunobu Kotani, Stefanie Tellex, and James Tompkin. 2020. Generating handwriting via decoupled style descriptors. In Proceedings of the European Conference on Computer Vision (ECCV’20). 764–780.

Brenden M. Lake, Ruslan Salakhutdinov, and Joshua B. Tenenbaum. 2015. Humanlevel concept learning through probabilistic program induction. Science 350, 6266 (2015), 1332–1338. https://doi.org/10.1126/science.aab3050

Bart Lamiroy, Thomas Bouville, Julien Blégean, Hongliu Cao, Salah Ghamizi, Romain Houpin, and Matthias Lloyd. 2015. Re-typograph phase I: A proof-of-concept for typeface parameter extraction from historical documents. In Document Recognition and Retrieval XXII, Eric K. Ringger and Bart Lamiroy (Eds.), Vol. 9402. International Society for Optics and Photonics, SPIE, 80–91. DOI:10.1117/12.2075813

Longin Jan Latecki and Rolf Lakämper. 1998. Discrete approach to curve evolution. In Mustererkennung 1998. Springer, 85–92. https://doi.org/10.1007/978-3-642-72282- 0\_7

R. L. Levien. 2009. From Spiral to Spline: Optimal Techniques in Interactive Curve Design. Ph.D. Dissertation. EECS Department, University of California, Berkeley.

Michael Leyton. 1987. Symmetry-curvature duality. Comput. Vis. Graph. Image Process. 38, 3 (1987), 327–341. https://doi.org/10.1016/0734-189X(86)90087-3

Michael Leyton. 1988. A process-grammar for shape. Artif. Intell. 34, 2 (March 1988), 213–247. https://doi.org/10.1016/0004-3702(88)90039-2

Lei Luo, Chunhua Shen, Xinwang Liu, and Chunyuan Zhang. 2015. A computational model of the short-cut rule for 2D shape decomposition. IEEE Trans. Image Process. 24, 1 (2015), 273–283. https://doi.org/10.1109/TIP.2014.2376188

Diego Macrini, Sven Dickinson, David Fleet, and Kaleem Siddiqi. 2011. Bone graphs: Medial shape parsing and abstraction. Comput. Vis. Image Understand. 115, 7 (July 2011), 1044–1061. https://doi.org/10.1016/j.cviu.2010.12.011

Diego Macrini, Kaleem Siddiqi, and Sven Dickinson. 2008. From skeletons to bone graphs: Medial abstraction for object recognition. In Proceedings of the IEEE Conference on Computer Vision and Pattern Recognition (CVPR’08). https://doi.org/ 10.1109/CVPR.2008.4587790

Xiaofeng Mi and Doug DeCarlo. 2007. Separating parts from 2D shapes using relatability. In Proceedings of the IEEE 11th International Conference on Computer Vision (ICCV’07). https://doi.org/10.1109/ICCV.2007.4409014

Martin Nöllenburg. 2014. A survey on automated metro map layout methods. In Proceedings of the 1st Schematic Mapping Workshop. University of Essex, UK.

Gerrit Noordzij. 2005. The Stroke—Theory of Writing. Hyphen Press. Translated from the Dutch original of 1985 by Peter Enneson.

Robert L. Ogniewicz and Markus Ilg. 1992. Voronoi skeletons: Theory and applications. In Proceedings of the IEEE Conference on Computer Vision and Pattern Recognition (CVPR’92). 63–69. https://doi.org/10.1109/CVPR.1992.223226

Nikos Papanelopoulos, Yannis Avrithis, and Stefanos Kollias. 2019. Revisiting the medial axis for planar shape decomposition. Comput. Vis. Image Understand. 179 (2019), 66–78. https://doi.org/10.1016/j.cviu.2018.10.007

Pierre Parent and Steven W. Zucker. 1989. Trace inference, curvature consistency, and curve detection. IEEE Trans. Pattern Anal. Mach. Intell. 11, 8 (1989), 823–839. https: //doi.org/10.1109/34.31445

Huy Quoc Phan, Hongbo Fu, and Antoni B Chan. 2015. Flexyfont: Learning transferring rules for flexible typeface synthesis. In Computer Graphics Forum, Vol. 34. 245–256. https://doi.org/10.1111/cgf.12763

R. Plamondon and S. N. Srihari. 2000. Online and off-line handwriting recognition: A comprehensive survey. IEEE Trans. Pattern Anal. Mach. Intell. 22, 1 (2000), 63–84. https://doi.org/10.1109/34.824821

Franco P. Preparata and Michael Ian Shamos. 1985. Intersections. 266–322. https://doi. org/10.1007/978-1-4612-1098-6\_7

Hock Soon Seah, Zhongke Wu, Feng Tian, Xian Xiao, and Boya Xie. 2005. Artistic brushstroke representation and animation with disk B-spline curve. In Proceedings of the ACM SIGCHI International Conference on Advances in Computer Entertainment Technology. 88–93. https://doi.org/10.1145/1178477.1178489

Doron Shaked and Alfred M Bruckstein. 1998. Pruning medial axes. Comput. Vis. Image Understand. 69, 2 (1998), 156–169. https://doi.org/10.1006/cviu.1997.0598

Ariel Shamir. 2003. Constraint-based approach for automatic hinting of digital typefaces. ACM Trans. Graph. 22, 2 (2003), 131–151. https://doi.org/10.1145/636886. 636887

Ariel Shamir and Ari Rappoport. 1996. Extraction of typographic elements from outline representations of fonts. Comput. Graph. Forum 15, 3 (1996), 259–268. https://doi.org/10.1111/1467-8659.1530259

Kaleem Siddiqi and Benjamin B. Kimia. 1995. Parts of visual form: Computational aspects. IEEE Trans. Pattern Anal. Mach. Intell. 17, 3 (1995), 239–251. https://doi. org/10.1109/34.368189

Manish Singh and Donald D. Hoffman. 2001. Part-based representations of visual shape and implications for visual cognition. In Advances in Psychology. Vol. 130. 401–459. https://doi.org/10.1016/S0166-4115(01)80033-9

Manish Singh, Gregory D. Seyranian, and Donald D. Hoffman. 1999. Parsing silhouettes: The short-cut rule. Percept. Psychophys. 61, 4 (1999), 636–660. https: //doi.org/10.3758/BF03205536

Patrick Spröte, Filipp Schmidt, and Roland W. Fleming. 2016. Visual perception of shape altered by inferred causal history. Sci. Rep. 6, 36245 (2016). https://doi.org/ 10.1038/srep36245

Yuandong Sun, Huihuan Qian, and Yangsheng Xu. 2014. A geometric approach to stroke extraction for the chinese calligraphy robot. In Proceedings of the IEEE International Conference on Robotics and Automation (ICRA’14). 3207–3212. https: //doi.org/10.1109/ICRA.2014.6907320

Rapee Suveeranont and Takeo Igarashi. 2010. Example-based automatic font generation. In Smart Graphics. Lecture Notes in Computer Science, Vol. 6133. 127–138. https://doi.org/10.1007/978-3-642-13544-6\_12

Fan Tang, Weiming Dong, Yiping Meng, Xing Mei, Feiyue Huang, Xiaopeng Zhang, and Oliver Deussen. 2017. Animated construction of chinese brush paintings. IEEE Trans. Vis. Comput. Graph. 24, 12 (2017), 3019–3031. https://doi.org/10.1109/ TVCG.2017.2774292

S. P. Timoshenko and J. N. Goodier. 1951. Theory of Elasticity. McGraw–Hill.

Johan Wagemans. 2018. Perceptual organization. In Stevens’ Handbook of Experimental Psychology and Cognitive Neuroscience, Sensation, Perception, and Attention. Vol. 2. Chapter 18, 803–872. https://doi.org/10.1002/9781119170174.epcn218 4th Edition.

Johan Wagemans, Andrea J. van Doorn, and Jan J. Koenderink. 2011. Measuring 3D point configurations in pictorial space. i-Perception 2, 1 (2011), 77–111. https://doi. org/10.1068/i0420

Jue Wang, Chenyu Wu, Ying-Qing Xu, Heung-Yeung Shum, and Liang Ji. 2002. Learning-based cursive handwriting synthesis. In Proceedings of the 8th IEEE International Workshop on Frontiers in Handwriting Recognition. 157–162. https: //doi.org/10.1109/IWFHR.2002.1030902

Yue Wang. 2013. Interview with Charles Bigelow. TUGboat 34, 2 (2013), 136–167.

Carl-Fredrik Westin, Stephan E Maier, Hatsuho Mamata, Arya Nabavi, Ferenc A Jolesz, and Ron Kikinis. 2002. Processing and visualization for diffusion tensor MRI. Med. Image Anal. 6, 2 (2002), 93–108. https://doi.org/10.1016/S1361-8415(02)00053-1

Lance Williams and Karvel K. Thornber. 2001. Orientation, scale, and discontinuity as emergent properties of illusory contour shape. Neural Comput. 13, 8 (August 2001), 1683–1711. https://doi.org/10.1162/08997660152469305

Songhua Xu, Hao Jiang, Francis C. M. Lau, and Yunhe Pan. 2012. Computationally evaluating and reproducing the beauty of chinese calligraphy. IEEE Intell. Syst. 3 (2012), 63–72. https://doi.org/10.1109/MIS.2012.46

Yaoda Xu and Manish Singh. 2002. Early computation of part structure: Evidence from visual search. Percept. Psychophys. 64, 7 (2002), 1039–1054. https://doi.org/10.3758/ BF03194755

Shih Cheng Yen and Leif H. Finkel. 1998. Extraction of perceptually salient contours by striate cortical networks. Vis. Res. 38, 5 (1998), 719–741. https://doi.org/10.1016/ S0042-6989(97)00197-1

Junsong Zhang, Yu Wang, Weiyi Xiao, and Zhenshan Luo. 2017. Synthesizing ornamental typefaces. Comput. Graph. Forum 36, 1 (2017), 64–75. https://doi.org/10. 1111/cgf.12785

Zhiyuan Zhao and Alan Saalfeld. 1997. Linear-time sleeve-fitting polyline simplification algorithms. In Proceedings of the 13th AutoCarto Symposium, Vol. 13. 214–223. https://cartogis.org

Changqing Zou, Junjie Cao, Warunika Ranaweera, Ibraheem Alhashim, Ping Tan, Alla Sheffer, and Hao Zhang. 2016. Legible compact calligrams. ACM Trans. Graph. 35, 4, Article 122 (2016), 12 pages. https://doi.org/10.1145/2897824.2925887 Article no. 122.

Received May 2020; revised September 2021; accepted December 2021