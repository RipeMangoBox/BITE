# HY3D-Bench: Generation of 3D Assets

\documentclass{article}
\usepackage{colm2024_conference}

\usepackage{booktabs}
\usepackage{graphicx}
\usepackage{enumitem}
\usepackage{wrapfig}
\usepackage{algorithm}
\usepackage{algpseudocode}
\usepackage{wrapfig}
\usepackage{float}
\usepackage{microtype}
\usepackage{amsmath}
\usepackage{amssymb}
\usepackage{colortbl}
\usepackage[utf8]{inputenc}
\definecolor{lightgray}{rgb}{0.9,0.9,0.9}
\usepackage{caption}
\usepackage{subcaption}
\usepackage{xcolor}
\usepackage{setspace}
\usepackage{url}
\usepackage{multirow}
\usepackage{colortbl}
\usepackage{tabularx}
\usepackage{blindtext}
\usepackage{pgfplots}
\pgfplotsset{compat=1.18}
\usepackage{tikz}
\usetikzlibrary{er,positioning,bayesnet}
\usepackage{makecell}
\usepackage{tipa}
\usepackage{siunitx}
\usepackage{nicefrac}
\usepackage{tocloft}
\usepackage{listings}
\usepackage[raster,skins]{tcolorbox}
\usepackage{xltabular}
\usepackage{adjustbox}
\usepackage{xurl}
\usepackage{multicol}

\usepackage{amsmath,amsfonts,bm}

\newcommand{\figleft}{{\em (Left)}}
\newcommand{\figcenter}{{\em (Center)}}
\newcommand{\figright}{{\em (Right)}}
\newcommand{\figtop}{{\em (Top)}}
\newcommand{\figbottom}{{\em (Bottom)}}
\newcommand{\captiona}{{\em (a)}}
\newcommand{\captionb}{{\em (b)}}
\newcommand{\captionc}{{\em (c)}}
\newcommand{\captiond}{{\em (d)}}

\newcommand{\newterm}[1]{{\bf #1}}


\def\figref#1{figure~\ref{#1}}
\def\Figref#1{Figure~\ref{#1}}
\def\twofigref#1#2{figures \ref{#1} and \ref{#2}}
\def\quadfigref#1#2#3#4{figures \ref{#1}, \ref{#2}, \ref{#3} and \ref{#4}}
\def\secref#1{section~\ref{#1}}
\def\Secref#1{Section~\ref{#1}}
\def\twosecrefs#1#2{sections \ref{#1} and \ref{#2}}
\def\secrefs#1#2#3{sections \ref{#1}, \ref{#2} and \ref{#3}}
\def\eqref#1{equation~\ref{#1}}
\def\Eqref#1{Equation~\ref{#1}}
\def\plaineqref#1{\ref{#1}}
\def\chapref#1{chapter~\ref{#1}}
\def\Chapref#1{Chapter~\ref{#1}}
\def\rangechapref#1#2{chapters\ref{#1}--\ref{#2}}
\def\algref#1{algorithm~\ref{#1}}
\def\Algref#1{Algorithm~\ref{#1}}
\def\twoalgref#1#2{algorithms \ref{#1} and \ref{#2}}
\def\Twoalgref#1#2{Algorithms \ref{#1} and \ref{#2}}
\def\partref#1{part~\ref{#1}}
\def\Partref#1{Part~\ref{#1}}
\def\twopartref#1#2{parts \ref{#1} and \ref{#2}}

\def\ceil#1{\lceil #1 \rceil}
\def\floor#1{\lfloor #1 \rfloor}
\def\1{\bm{1}}
\newcommand{\train}{\mathcal{D}}
\newcommand{\valid}{\mathcal{D_{\mathrm{valid}}}}
\newcommand{\test}{\mathcal{D_{\mathrm{test}}}}

\def\eps{{\epsilon}}


\def\reta{{\textnormal{$\eta$}}}
\def\ra{{\textnormal{a}}}
\def\rb{{\textnormal{b}}}
\def\rc{{\textnormal{c}}}
\def\rd{{\textnormal{d}}}
\def\re{{\textnormal{e}}}
\def\rf{{\textnormal{f}}}
\def\rg{{\textnormal{g}}}
\def\rh{{\textnormal{h}}}
\def\ri{{\textnormal{i}}}
\def\rj{{\textnormal{j}}}
\def\rk{{\textnormal{k}}}
\def\rl{{\textnormal{l}}}
\def\rn{{\textnormal{n}}}
\def\ro{{\textnormal{o}}}
\def\rp{{\textnormal{p}}}
\def\rq{{\textnormal{q}}}
\def\rr{{\textnormal{r}}}
\def\rs{{\textnormal{s}}}
\def\rt{{\textnormal{t}}}
\def\ru{{\textnormal{u}}}
\def\rv{{\textnormal{v}}}
\def\rw{{\textnormal{w}}}
\def\rx{{\textnormal{x}}}
\def\ry{{\textnormal{y}}}
\def\rz{{\textnormal{z}}}

\def\rvepsilon{{\mathbf{\epsilon}}}
\def\rvtheta{{\mathbf{\theta}}}
\def\rva{{\mathbf{a}}}
\def\rvb{{\mathbf{b}}}
\def\rvc{{\mathbf{c}}}
\def\rvd{{\mathbf{d}}}
\def\rve{{\mathbf{e}}}
\def\rvf{{\mathbf{f}}}
\def\rvg{{\mathbf{g}}}
\def\rvh{{\mathbf{h}}}
\def\rvu{{\mathbf{i}}}
\def\rvj{{\mathbf{j}}}
\def\rvk{{\mathbf{k}}}
\def\rvl{{\mathbf{l}}}
\def\rvm{{\mathbf{m}}}
\def\rvn{{\mathbf{n}}}
\def\rvo{{\mathbf{o}}}
\def\rvp{{\mathbf{p}}}
\def\rvq{{\mathbf{q}}}
\def\rvr{{\mathbf{r}}}
\def\rvs{{\mathbf{s}}}
\def\rvt{{\mathbf{t}}}
\def\rvu{{\mathbf{u}}}
\def\rvv{{\mathbf{v}}}
\def\rvw{{\mathbf{w}}}
\def\rvx{{\mathbf{x}}}
\def\rvy{{\mathbf{y}}}
\def\rvz{{\mathbf{z}}}

\def\erva{{\textnormal{a}}}
\def\ervb{{\textnormal{b}}}
\def\ervc{{\textnormal{c}}}
\def\ervd{{\textnormal{d}}}
\def\erve{{\textnormal{e}}}
\def\ervf{{\textnormal{f}}}
\def\ervg{{\textnormal{g}}}
\def\ervh{{\textnormal{h}}}
\def\ervi{{\textnormal{i}}}
\def\ervj{{\textnormal{j}}}
\def\ervk{{\textnormal{k}}}
\def\ervl{{\textnormal{l}}}
\def\ervm{{\textnormal{m}}}
\def\ervn{{\textnormal{n}}}
\def\ervo{{\textnormal{o}}}
\def\ervp{{\textnormal{p}}}
\def\ervq{{\textnormal{q}}}
\def\ervr{{\textnormal{r}}}
\def\ervs{{\textnormal{s}}}
\def\ervt{{\textnormal{t}}}
\def\ervu{{\textnormal{u}}}
\def\ervv{{\textnormal{v}}}
\def\ervw{{\textnormal{w}}}
\def\ervx{{\textnormal{x}}}
\def\ervy{{\textnormal{y}}}
\def\ervz{{\textnormal{z}}}

\def\rmA{{\mathbf{A}}}
\def\rmB{{\mathbf{B}}}
\def\rmC{{\mathbf{C}}}
\def\rmD{{\mathbf{D}}}
\def\rmE{{\mathbf{E}}}
\def\rmF{{\mathbf{F}}}
\def\rmG{{\mathbf{G}}}
\def\rmH{{\mathbf{H}}}
\def\rmI{{\mathbf{I}}}
\def\rmJ{{\mathbf{J}}}
\def\rmK{{\mathbf{K}}}
\def\rmL{{\mathbf{L}}}
\def\rmM{{\mathbf{M}}}
\def\rmN{{\mathbf{N}}}
\def\rmO{{\mathbf{O}}}
\def\rmP{{\mathbf{P}}}
\def\rmQ{{\mathbf{Q}}}
\def\rmR{{\mathbf{R}}}
\def\rmS{{\mathbf{S}}}
\def\rmT{{\mathbf{T}}}
\def\rmU{{\mathbf{U}}}
\def\rmV{{\mathbf{V}}}
\def\rmW{{\mathbf{W}}}
\def\rmX{{\mathbf{X}}}
\def\rmY{{\mathbf{Y}}}
\def\rmZ{{\mathbf{Z}}}

\def\ermA{{\textnormal{A}}}
\def\ermB{{\textnormal{B}}}
\def\ermC{{\textnormal{C}}}
\def\ermD{{\textnormal{D}}}
\def\ermE{{\textnormal{E}}}
\def\ermF{{\textnormal{F}}}
\def\ermG{{\textnormal{G}}}
\def\ermH{{\textnormal{H}}}
\def\ermI{{\textnormal{I}}}
\def\ermJ{{\textnormal{J}}}
\def\ermK{{\textnormal{K}}}
\def\ermL{{\textnormal{L}}}
\def\ermM{{\textnormal{M}}}
\def\ermN{{\textnormal{N}}}
\def\ermO{{\textnormal{O}}}
\def\ermP{{\textnormal{P}}}
\def\ermQ{{\textnormal{Q}}}
\def\ermR{{\textnormal{R}}}
\def\ermS{{\textnormal{S}}}
\def\ermT{{\textnormal{T}}}
\def\ermU{{\textnormal{U}}}
\def\ermV{{\textnormal{V}}}
\def\ermW{{\textnormal{W}}}
\def\ermX{{\textnormal{X}}}
\def\ermY{{\textnormal{Y}}}
\def\ermZ{{\textnormal{Z}}}

\def\vzero{{\bm{0}}}
\def\vone{{\bm{1}}}
\def\vmu{{\bm{\mu}}}
\def\vtheta{{\bm{\theta}}}
\def\va{{\bm{a}}}
\def\vb{{\bm{b}}}
\def\vc{{\bm{c}}}
\def\vd{{\bm{d}}}
\def\ve{{\bm{e}}}
\def\vf{{\bm{f}}}
\def\vg{{\bm{g}}}
\def\vh{{\bm{h}}}
\def\vi{{\bm{i}}}
\def\vj{{\bm{j}}}
\def\vk{{\bm{k}}}
\def\vl{{\bm{l}}}
\def\vm{{\bm{m}}}
\def\vn{{\bm{n}}}
\def\vo{{\bm{o}}}
\def\vp{{\bm{p}}}
\def\vq{{\bm{q}}}
\def\vr{{\bm{r}}}
\def\vs{{\bm{s}}}
\def\vt{{\bm{t}}}
\def\vu{{\bm{u}}}
\def\vv{{\bm{v}}}
\def\vw{{\bm{w}}}
\def\vx{{\bm{x}}}
\def\vy{{\bm{y}}}
\def\vz{{\bm{z}}}

\def\evalpha{{\alpha}}
\def\evbeta{{\beta}}
\def\evepsilon{{\epsilon}}
\def\evlambda{{\lambda}}
\def\evomega{{\omega}}
\def\evmu{{\mu}}
\def\evpsi{{\psi}}
\def\evsigma{{\sigma}}
\def\evtheta{{\theta}}
\def\eva{{a}}
\def\evb{{b}}
\def\evc{{c}}
\def\evd{{d}}
\def\eve{{e}}
\def\evf{{f}}
\def\evg{{g}}
\def\evh{{h}}
\def\evi{{i}}
\def\evj{{j}}
\def\evk{{k}}
\def\evl{{l}}
\def\evm{{m}}
\def\evn{{n}}
\def\evo{{o}}
\def\evp{{p}}
\def\evq{{q}}
\def\evr{{r}}
\def\evs{{s}}
\def\evt{{t}}
\def\evu{{u}}
\def\evv{{v}}
\def\evw{{w}}
\def\evx{{x}}
\def\evy{{y}}
\def\evz{{z}}

\def\mA{{\bm{A}}}
\def\mB{{\bm{B}}}
\def\mC{{\bm{C}}}
\def\mD{{\bm{D}}}
\def\mE{{\bm{E}}}
\def\mF{{\bm{F}}}
\def\mG{{\bm{G}}}
\def\mH{{\bm{H}}}
\def\mI{{\bm{I}}}
\def\mJ{{\bm{J}}}
\def\mK{{\bm{K}}}
\def\mL{{\bm{L}}}
\def\mM{{\bm{M}}}
\def\mN{{\bm{N}}}
\def\mO{{\bm{O}}}
\def\mP{{\bm{P}}}
\def\mQ{{\bm{Q}}}
\def\mR{{\bm{R}}}
\def\mS{{\bm{S}}}
\def\mT{{\bm{T}}}
\def\mU{{\bm{U}}}
\def\mV{{\bm{V}}}
\def\mW{{\bm{W}}}
\def\mX{{\bm{X}}}
\def\mY{{\bm{Y}}}
\def\mZ{{\bm{Z}}}
\def\mBeta{{\bm{\beta}}}
\def\mPhi{{\bm{\Phi}}}
\def\mLambda{{\bm{\Lambda}}}
\def\mSigma{{\bm{\Sigma}}}

\DeclareMathAlphabet{\mathsfit}{\encodingdefault}{\sfdefault}{m}{sl}
\SetMathAlphabet{\mathsfit}{bold}{\encodingdefault}{\sfdefault}{bx}{n}
\newcommand{\tens}[1]{\bm{\mathsfit{#1}}}
\def\tA{{\tens{A}}}
\def\tB{{\tens{B}}}
\def\tC{{\tens{C}}}
\def\tD{{\tens{D}}}
\def\tE{{\tens{E}}}
\def\tF{{\tens{F}}}
\def\tG{{\tens{G}}}
\def\tH{{\tens{H}}}
\def\tI{{\tens{I}}}
\def\tJ{{\tens{J}}}
\def\tK{{\tens{K}}}
\def\tL{{\tens{L}}}
\def\tM{{\tens{M}}}
\def\tN{{\tens{N}}}
\def\tO{{\tens{O}}}
\def\tP{{\tens{P}}}
\def\tQ{{\tens{Q}}}
\def\tR{{\tens{R}}}
\def\tS{{\tens{S}}}
\def\tT{{\tens{T}}}
\def\tU{{\tens{U}}}
\def\tV{{\tens{V}}}
\def\tW{{\tens{W}}}
\def\tX{{\tens{X}}}
\def\tY{{\tens{Y}}}
\def\tZ{{\tens{Z}}}


\def\gA{{\mathcal{A}}}
\def\gB{{\mathcal{B}}}
\def\gC{{\mathcal{C}}}
\def\gD{{\mathcal{D}}}
\def\gE{{\mathcal{E}}}
\def\gF{{\mathcal{F}}}
\def\gG{{\mathcal{G}}}
\def\gH{{\mathcal{H}}}
\def\gI{{\mathcal{I}}}
\def\gJ{{\mathcal{J}}}
\def\gK{{\mathcal{K}}}
\def\gL{{\mathcal{L}}}
\def\gM{{\mathcal{M}}}
\def\gN{{\mathcal{N}}}
\def\gO{{\mathcal{O}}}
\def\gP{{\mathcal{P}}}
\def\gQ{{\mathcal{Q}}}
\def\gR{{\mathcal{R}}}
\def\gS{{\mathcal{S}}}
\def\gT{{\mathcal{T}}}
\def\gU{{\mathcal{U}}}
\def\gV{{\mathcal{V}}}
\def\gW{{\mathcal{W}}}
\def\gX{{\mathcal{X}}}
\def\gY{{\mathcal{Y}}}
\def\gZ{{\mathcal{Z}}}

\def\sA{{\mathbb{A}}}
\def\sB{{\mathbb{B}}}
\def\sC{{\mathbb{C}}}
\def\sD{{\mathbb{D}}}
\def\sF{{\mathbb{F}}}
\def\sG{{\mathbb{G}}}
\def\sH{{\mathbb{H}}}
\def\sI{{\mathbb{I}}}
\def\sJ{{\mathbb{J}}}
\def\sK{{\mathbb{K}}}
\def\sL{{\mathbb{L}}}
\def\sM{{\mathbb{M}}}
\def\sN{{\mathbb{N}}}
\def\sO{{\mathbb{O}}}
\def\sP{{\mathbb{P}}}
\def\sQ{{\mathbb{Q}}}
\def\sR{{\mathbb{R}}}
\def\sS{{\mathbb{S}}}
\def\sT{{\mathbb{T}}}
\def\sU{{\mathbb{U}}}
\def\sV{{\mathbb{V}}}
\def\sW{{\mathbb{W}}}
\def\sX{{\mathbb{X}}}
\def\sY{{\mathbb{Y}}}
\def\sZ{{\mathbb{Z}}}

\def\emLambda{{\Lambda}}
\def\emA{{A}}
\def\emB{{B}}
\def\emC{{C}}
\def\emD{{D}}
\def\emE{{E}}
\def\emF{{F}}
\def\emG{{G}}
\def\emH{{H}}
\def\emI{{I}}
\def\emJ{{J}}
\def\emK{{K}}
\def\emL{{L}}
\def\emM{{M}}
\def\emN{{N}}
\def\emO{{O}}
\def\emP{{P}}
\def\emQ{{Q}}
\def\emR{{R}}
\def\emS{{S}}
\def\emT{{T}}
\def\emU{{U}}
\def\emV{{V}}
\def\emW{{W}}
\def\emX{{X}}
\def\emY{{Y}}
\def\emZ{{Z}}
\def\emSigma{{\Sigma}}

\newcommand{\etens}[1]{\mathsfit{#1}}
\def\etLambda{{\etens{\Lambda}}}
\def\etA{{\etens{A}}}
\def\etB{{\etens{B}}}
\def\etC{{\etens{C}}}
\def\etD{{\etens{D}}}
\def\etE{{\etens{E}}}
\def\etF{{\etens{F}}}
\def\etG{{\etens{G}}}
\def\etH{{\etens{H}}}
\def\etI{{\etens{I}}}
\def\etJ{{\etens{J}}}
\def\etK{{\etens{K}}}
\def\etL{{\etens{L}}}
\def\etM{{\etens{M}}}
\def\etN{{\etens{N}}}
\def\etO{{\etens{O}}}
\def\etP{{\etens{P}}}
\def\etQ{{\etens{Q}}}
\def\etR{{\etens{R}}}
\def\etS{{\etens{S}}}
\def\etT{{\etens{T}}}
\def\etU{{\etens{U}}}
\def\etV{{\etens{V}}}
\def\etW{{\etens{W}}}
\def\etX{{\etens{X}}}
\def\etY{{\etens{Y}}}
\def\etZ{{\etens{Z}}}

\newcommand{\pdata}{p_{\rm{data}}}
\newcommand{\ptrain}{\hat{p}_{\rm{data}}}
\newcommand{\Ptrain}{\hat{P}_{\rm{data}}}
\newcommand{\pmodel}{p_{\rm{model}}}
\newcommand{\Pmodel}{P_{\rm{model}}}
\newcommand{\ptildemodel}{\tilde{p}_{\rm{model}}}
\newcommand{\pencode}{p_{\rm{encoder}}}
\newcommand{\pdecode}{p_{\rm{decoder}}}
\newcommand{\precons}{p_{\rm{reconstruct}}}

\newcommand{\laplace}{\mathrm{Laplace}}

\newcommand{\E}{\mathbb{E}}
\newcommand{\Ls}{\mathcal{L}}
\newcommand{\R}{\mathbb{R}}
\newcommand{\emp}{\tilde{p}}
\newcommand{\lr}{\alpha}
\newcommand{\reg}{\lambda}
\newcommand{\rect}{\mathrm{rectifier}}
\newcommand{\softmax}{\mathrm{softmax}}
\newcommand{\sigmoid}{\sigma}
\newcommand{\softplus}{\zeta}
\newcommand{\KL}{D_{\mathrm{KL}}}
\newcommand{\Var}{\mathrm{Var}}
\newcommand{\standarderror}{\mathrm{SE}}
\newcommand{\Cov}{\mathrm{Cov}}
\newcommand{\normlzero}{L^0}
\newcommand{\normlone}{L^1}
\newcommand{\normltwo}{L^2}
\newcommand{\normlp}{L^p}
\newcommand{\normmax}{L^\infty}

\newcommand{\parents}{Pa}

\DeclareMathOperator*{\argmax}{arg\,max}
\DeclareMathOperator*{\argmin}{arg\,min}

\DeclareMathOperator{\sign}{sign}
\DeclareMathOperator{\Tr}{Tr}
\let\ab\allowbreak


\newcommand{\specialcell}[2][c]{
  \begin{tabular}[#1]{@{}c@{}}#2\end{tabular}}

\makeatletter
\DeclareRobustCommand\onedot{\futurelet\@let@token\@onedot}
\def\@onedot{\ifx\@let@token.\else.\null\fi\xspace}

\def\eg{\emph{e.g}\onedot} \def\Eg{\emph{E.g}\onedot}
\def\ie{\emph{i.e}\onedot} \def\Ie{\emph{I.e}\onedot}
\def\cf{\emph{cf}\onedot} \def\Cf{\emph{Cf}\onedot}
\def\etc{\emph{etc}\onedot} \def\vs{\emph{vs}\onedot}
\def\wrt{w.r.t\onedot} \def\dof{d.o.f\onedot}
\def\iid{i.i.d\onedot} \def\wolog{w.l.o.g\onedot}
\def\etal{\emph{et al}\onedot}
\makeatother


\newcommand{\fix}{\marginpar{FIX}}
\newcommand{\new}{\marginpar{NEW}}
\newcommand{\shortname}{HY3D-Bench\xspace}
\newcommand{\yunhan}[1]{\textcolor{red}{[Yunhan: #1]}}
\newcommand{\kunb}[1]{\textcolor{blue}{[Kunhong: #1]}}

\title{\shortname: Generation of 3D Assets}


\author{
\bf Tencent Hunyuan3D
}


\begin{document}

\maketitle

\begin{figure}[h]
\centering
\includegraphics[width=0.99\linewidth]{figures/teaser.pdf}
\caption{HY3D-Bench is a unified ecosystem for high-fidelity 3D content generation. Our framework introduces (a) 252k high-quality assets with watertight meshes and multi-view renderings, (b) 240k structured part-level decomposition enabling fine-grained control, and (c) AIGC-synthesized 125k long-tail category assets. This benchmark provides standardized training data and evaluation protocols for advancing 3D generation research.}

\label{fig:teaser-top}
\end{figure}

\begin{abstract}
While recent advances in neural representations and generative models have revolutionized 3D content creation, the field remains constrained by significant data processing bottlenecks. To address this, we introduce HY3D-Bench, an open-source ecosystem designed to establish a unified, high-quality foundation for 3D generation. Our contributions are threefold: (1) We curate a library of 250k high-fidelity 3D objects distilled from large-scale repositories, employing a rigorous pipeline to deliver training-ready artifacts, including watertight meshes and multi-view renderings; (2) We introduce structured part-level decomposition, providing the granularity essential for fine-grained perception and controllable editing; and (3) We bridge real-world distribution gaps via a scalable AIGC synthesis pipeline, contributing 125k synthetic assets to enhance diversity in long-tail categories. Validated empirically through the training of Hunyuan3D-2.1-Small, HY3D-Bench democratizes access to robust data resources, aiming to catalyze innovation across 3D perception, robotics, and digital content creation.
\end{abstract}


\section{Introduction}

High-quality 3D content has become a critical asset across a broad range of fields, including 3D computer vision, generative modeling, and robotics. While pioneering large-scale repositories~\cite{objaverse,objaverseXL,wu2023omniobject3d} have provided an unprecedented volume of 3D data, their utility across these diverse fields is often hampered by significant limitations. Most raw assets in these datasets contain significant noise, non-manifold geometry, and a lack of structural granularity, which restricts their application in tasks requiring precise geometric understanding, stable generation, or complex robotic interaction.

In this work, we present \shortname, a comprehensive open-source ecosystem designed to provide a high-quality, structured, and reproducible foundation for 3D content research. Moving beyond simple mesh collection, our work integrates rigorous data engineering, standardized benchmarks, and scalable AIGC-driven synthesis to support the dual goals of 3D content understanding and creation. Our contributions are categorized into three major pillars:

First, we provide a \textbf{\textit{refined and structured 3D asset library}} with comprehensive data processing results. For each holistic object, we implement a professional pipeline to generate \textit{training-ready} assets featuring the \textit{best watertight mesh} and high-fidelity rendered images, both of which are essential for stable 3D generation training and accurate geometric perception. Crucially, we utilize a part-merging strategy to produce structured assets with consistent part-level decomposition. For the structural components, we provide the original mesh segmentation results and individual part-level watertight meshes, complemented by view-dependent RGB renderings and 2D masks for the integrated part assembly. This structural granularity provides the necessary information for part-aware generation and fine-grained perception tasks.

Second, we establish a \textbf{\textit{standardized evaluation and experiment framework}} to address the fragmentation in 3D research. We propose a rigorous benchmark comprising 400 high-quality objects across diverse categories, providing a unified platform for testing 3D generation algorithms. Unlike previous works with inconsistent evaluation protocols, we provide a complete suite of standard metrics, baselines, and a fixed experiment setting. By releasing our standardized training configurations and pre-trained model checkpoints, we empower the community to conduct fair comparisons and accelerate the rapid advancement of the 3D generation field.

Third, we introduce a \textbf{\textit{scalable AIGC-driven data synthesis pipeline}} to bridge the gap in category diversity and long-tail distribution. Recognizing that manual 3D modeling for realistic scenarios, such as shopping malls, is prohibitively expensive, we leverage the generative power of Large Language Models and Diffusion Models to synthesize diverse 3D content. Our three-step paradigm, consisting of Text-to-Text for semantic expansion, Text-to-Image for visual synthesis, and Image-to-3D for mesh reconstruction, allows us to produce a vast collection of long-tail items, allows us to produce a vast collection of long-tail items covering 20 super-categories, 130 categories, and 1,252 fine-grained sub-categories. This synthetic data provides a critical supplement for training models that can generalize to rare but crucial object categories, which is particularly vital for the robustness of generation and the diversity of robotics simulation environments.

By providing a structured, diverse, and standardized 3D content ecosystem, we aim to lower the barrier for research and drive the progress toward a unified understanding and generation of the 3D world. In summary, our contributions are as follows:
\begin{itemize}
    \item A high-quality 3D asset library featuring watertight meshes and rendered images for both holistic objects and parts.
    \item A standardized 3D benchmark and experiment framework, providing unified metrics, baselines, and model weights.
    \item An AIGC-based synthesis framework that expands 3D data diversity, focusing on long-tail assets to support broad generalization.
    \item Extensive data and infrastructure support for a wide range of downstream tasks, including 3D generation, perception pre-training, and robotics simulation.
\end{itemize}









\section{Related Work}

\begin{figure}
    \centering
    \includegraphics[width=0.9\linewidth]{figures/related_methods_overview.pdf}
    \caption{The evolution of the 3D generation.}
    \label{fig:related}
\end{figure}

\subsection{3D Generation}
The field of 3D generation has emerged as a cornerstone of generative AI, bridging the gap between virtual content creation and real-world applications. The evolution of 3D generation has witnessed a paradigm shift from manual modeling and scanning-based reconstruction to data-driven AI synthesis. This field can be systematically categorized into four major paradigms: GAN-based methods, SDS-based methods, feedforward-based methods, and 3D native generation, as shown in Figure~\ref{fig:related}.

{\bf GAN-based generation.} Generative Adversarial Networks (GANs)~\cite{goodfellow2020generative} established the initial paradigm for high-fidelity synthesis by optimizing a minimax objective between a generator and a discriminator.
Following this, early works~\cite{luo2021surfgen,chen2022gdna} based on explicit representations, such as voxel grids~\cite{wu2016learning,nguyen2020blockgan,nguyen2019hologan} and point clouds~\cite{shu20193d,li2021sp}, attempt to generate 3D shapes directly, yet methods often suffer from cubic memory complexity and limited resolution.
The advent of Neural Radiance Fields (NeRF)~\cite{mildenhall2021nerf} shifted the focus toward 3D-aware image synthesis, where models are trained on multi-view 2D images to learn underlying 3D geometry.
Seminal works such as GRAF~\cite{schwarz2020graf} and $\pi$-GAN~\cite{chan2021pi} integrated conditional radiance fields with adversarial training, utilizing coordinate-based MLPs to enforce multi-view consistency.
However, fully implicit backbones proved computationally expensive for high-resolution rendering.
Addressing this, EG3D~\cite{chan2022efficient} proposed a hybrid explicit-implicit tri-plane representation, leveraging the efficiency of StyleGAN2~\cite{karras2020analyzing} to generate feature planes that are subsequently decoded by a lightweight MLP via volume rendering.
While GANs achieve rapid inference speeds, they remain prone to training instability and mode collapse, particularly when scaling to diverse, open-domain datasets.

{\bf SDS-based generation.}
The scarcity of large-scale, annotated 3D datasets has historically hindered the development of generative 3D models compared to their 2D counterparts. To circumvent this data bottleneck, recent approaches have shifted towards optimization-based pipelines that leverage pre-trained 2D text-to-image diffusion models as strong priors. The pioneer work, DreamFusion~\cite{poole2022dreamfusion}, introduced Score Distillation Sampling (SDS), a method that optimizes a differentiable 3D representation—typically a NeRF—such that its rendered views maintain high likelihood under a frozen 2D diffusion model. By replacing the standard diffusion denoising loss with a gradient-based score matching objective, SDS enables the distillation of semantic knowledge from 2D foundation models into consistent 3D structures without requiring 3D ground truth. Following DreamFusion, subsequent works~\cite{wang2023prolificdreamer,EnVision2023luciddreamer,fantasia3d,lin2023magic3d,sweetdreamer} are proposed to further enhance the quality of 3D generation. More recently, the field has transitioned from implicit NeRF representations to explicit 3D Gaussian Splatting \cite{kerbl20233d} to achieve real-time rendering and improved convergence speeds. Methods such as DreamGaussian~\cite{tang2023dreamgaussian} and GaussianDreamer\cite{yi2024gaussiandreamer} adapt SDS to optimize 3D Gaussian parameters, significantly reducing generation time while maintaining visual fidelity. However, these SDS-based methods usually suffer from the "Janus problem" (multi-face artifacts) due to the lack of explicit 3D geometry-related constraints. In addition, the problem of long-term optimization also poses real-time challenges for such methods.

{\bf Feedforward generation.} In contrast to optimization-based paradigms that require computationally expensive per-instance training (e.g., via Score Distillation Sampling), feedforward methods prioritize inference efficiency by learning a direct, amortized mapping from input prompts to 3D representations. A foundational direction in feedforward generation follows two stages: multi-view (MV) image synthesis and 3D reconstruction. For instance, MVDream~\cite{shimvdream} introduces a multi-view diffusion model conditioned on camera poses, enabling the generation of geometrically consistent MV images from text, which are then fed into a neural radiance field (NeRF) or mesh reconstruction pipeline to yield 3D assets. Subsequent methods~\cite{liu2023zero,long2024wonder3d,li2023instant3d,liu2023one,liu2023syncdreamer,li2024era3d} attempt to improve the multi-view consistency and image resolution to obtain high-quality 3D assets. Another prominent yet distinct feedforward paradigm for 3D generation is the Large Reconstruction Model (LRM) approach~\cite{hong2023lrm}. LRM aims to learn a universal reconstruction capability from large-scale 3D data, enabling it to generate 3D representations directly from textual or sparse visual inputs through a single forward pass. These models leverage the richness of large-scale 3D datasets to learn generalized 3D shape priors, which are then used to amortize the optimization cost across multiple generation tasks. Building on the LRM paradigm, subsequent works~\cite{wang2023pf,tang2024lgm,xu2024instantmesh,li2023instant3d} have proposed targeted improvements to enhance generation quality, efficiency, and generalization. For instance, LGM~\cite{tang2024lgm} proposes a representation based on Gaussian features to improve the resolution of 3D models. While these feedforward methods outperform optimization-based counterparts in inference speed and geometric quality, they are constrained by the resolution of 2D images and the lack of learning and understanding of the spatial distribution of 3D data, making it challenging to generate fine-grained and accurate 3D geometries.

{\bf Native generation.}
Unlike 2D-lifting approaches, native 3D generation methods directly learn the 3D representations, such as point clouds~\cite{zhou20213d,pointflow,nichol2022point,luo2021diffusion}, meshes~\cite{nash2020polygen,jun2023shap,Liu2023MeshDiffusion}, and implicit functions~\cite{chen2019learning,park2019deepsdf}, from large-scale 3D assets, typically yielding superior geometric consistency and topology. However, these non-compressed methods are typically constrained by computational complexity and resolution, making it challenging to generate high-quality geometries. A pivotal breakthrough in native 3D generation came with large-scale 3D datasets~\cite{objaverse,objaverseXL} and 3DShape2Vecset~\cite{zhang20233dshape2vecset}, which innovatively adopted the processing paradigm of 2D Stable Diffusion and constructed a 3D VAE (Variational Autoencoder) to compress 3D shapes into compact VecSet representation. With this representation, 3DShape2Vecset enabled the construction of diffusion models for both conditional and unconditional 3D generation. Following this workflow, subsequent works~\cite{zhao2024michelangelo,zhang2024clay,li2024craftsman,li2025triposg,wu2024direct3d,chen2025dora,hunyuan3d2025hunyuan3d} strive to enhance the model's generalization ability and geometric fidelity by scaling up the model and data. In contrast to implicit VexSet, several approaches~\cite{ren2024xcube,xiang2024structured,he2025sparseflex,wu2025direct3d,huang2025spar3d} apply structured voxel-based representation to preserve spatial structure in latent space. Additionally, there are a series of studies~\cite{dong2025crossgen,ye2025nano3d} that apply native generation on other specific issues. For example, PoseMaster~\cite{yan2025posemaster} and Hunyuan3D-Omni~\cite{hunyuan3d2025omni} introduce a native controllable generation model to achieve control on point, voxel, bounding box, and skeleton. There is also a line of research on fine-grained 3D generation, whose primary goal is to produce part-aware results. One set of works\cite{yang2025holopart,liu2023partslip,ma2025p3,kim2024partstad,zhong2024meshsegmenter,abdelreheem2023satr,tang2024segment,thai20243x2,xue2023zerops,yang2024sampart3d,liu2024part123, deng2025geosam2,zhou2024point,fischer2024sama,ma2025find,liu2025partfield,zhu2025partsam,paul2025name,li2025auto} adopts a segmentation-based pipeline: starting from a holistic object and decomposing it into parts via segmentation. Another set of works\cite{yan2025x,li2025moca,yang2025omnipart,lin2025partcrafter,tang2025efficient,dong2025one,ding2025fullpart,he2025unipart,yang2025partdiffuser} instead follows a part-aware generation paradigm, directly generating 3D objects with explicit part structures. In addition, some works~\cite{chang2015shapenet,mo2019partnet,collins2022abo,wang2025partnext,dong2025one,yang2024sampart3d,geng2023gapartnet,deng20213d} provide datasets with part-level annotations. While these methods present impressive performance in the 3D generation task, they usually rely on high-quality data processing in terms of the part-aware mesh and watertight mesh. In this paper, we open-source large-scale processed data that can be used to train 3D VAE and diffusion directly.




\subsection{3D Datasets}
The advancement of 3D generation models is inherently tied to the availability of high-quality benchmark datasets, which provide the foundational data support for model training, validation, and evaluation. Early 3D benchmark datasets~\cite{zhou2016thingi10k,fu20213d,downs2022google,wu2023omniobject3d}, such as ShapeNet~\cite{chang2015shapenet}, laid the initial groundwork for the development of 3D generation research. However, these datasets suffer from limitations such as a limited number of categories, simple geometry, and small quantities, which severely constrain the generalization capabilities of trained 3D generation models. This bottleneck has long restricted the further advancement of 3D generation technology towards more practical and versatile scenarios. The emergence of large-scale 3D datasets with complex geometric structures has broken this deadlock, among which Objaverse stands out as a pivotal milestone. As the large-scale, diverse 3D object dataset, Objaverse~\cite{objaverse} and Objaver-XL~\cite{objaverseXL} contain millions of 3D models spanning a wide range of categories, including complex geometric structures such as articulated objects, organic shapes, and detailed industrial parts. The release of Objaverse has significantly empowered the development of 3D generation technology, particularly fostering the advent of a new generation of large-scale 3D generation models.


However, a critical challenge persists in the current 3D generation research landscape: mainstream 3D generation models typically require extensive preprocessing of raw 3D data to generate task-specific representations, such as rendered images, watertight meshes, and corresponding Signed Distance Function (SDF) fields. This preprocessing step not only increases the entry barrier for researchers new to 3D generation, requiring proficiency in specialized data processing techniques, but also imposes substantial computational burdens. Although open-source data processing scripts have been developed to alleviate some of these difficulties by automating certain preprocessing workflows, processing large-scale training datasets (often involving millions of 3D models) demands enormous GPU and CPU computational resources. This resource-intensive preprocessing requirement remains a significant bottleneck for the broader research community, hindering the rapid iteration and widespread adoption of 3D generation models.

To address this critical challenge, in this paper, we directly provide a high-quality dataset of 200k samples specifically tailored for training 3D Variational Autoencoders (3D VAE) and 3D diffusion models. The data samples are curated from two large-scale 3D repositories, Objaverse and Objaverse-XL, ensuring rich category diversity and complex geometric characteristics. Notably, we process the 3D meshes to obtain watertight meshes at a resolution of 512, which effectively preserves a large number of fine-grained details from the original meshes. By offering this preprocessed, high-resolution 3D dataset, we aim to reduce the computational and technical burdens on researchers, lower the entry barrier for 3D generation research, and further facilitate the advancement of the field.


\section{Methods}



{\bf VAE}. Given an input point cloud $P \in R^{N \times (3 + C)}$ sampled from the mesh surface, where $C$ denotes surface normals, 3D VAE first extract point features and then obtain the corresponding latent vector set $Z \in R^{L \times d}$ via resampling from estimated distribution, where $L$ and $d$ indicate the length and dimension of latent VecSet, respectively. Subsequently, a decoder is applied to reconstruct the signed distance function (SDF) field $F_{sdf}$, in which we can leverage the iso-surface extraction to obtain explicit mesh output. The procedure of VAE can be formulated as follows:
\begin{align}
Z = \mathcal{E}(P), F_{sdf} = \mathcal{D}(Z)
\end{align}


{\bf Diffusion}. Given an image and its latent set representation $Z$ of a shape, the 3D diffusion model aims to model the denoising process, thereby achieving conditional generation from an arbitrary image. It first leverages an image encoder, such as DINO-v2~\cite{}, to capture image embeddings $c_i$ and then exploits the multi layers of DiT to predict the added noise or velocity. For a flow matching model used in Hunyuan3D 2.1~\cite{}, its training objective is to transform a simple noise distribution $x_0 \sim \mathcal{N}(0, I)$ into a complex data distribution $x_1 \sim D$ conditioned on image embeddings $c_i$, which can be formulated as follows:
\begin{equation}
\mathbb{E}_{t, {x}_0, {x_1}, c}\vert\vert{v}_\theta({x}, t, c)-(x_1-x_0)\vert\vert_2^2
\end{equation}






\section{Hunyuan Objarverse}





The currently open-source Objaverse series datasets~\cite{objaverse,objaverseXL} contain a vast collection of raw 3D assets available for access and download. However, these raw assets suffer from numerous critical issues that urgently need to be addressed, rendering them unsuitable for direct application in downstream tasks such as 3D generation.

First, from a technical specification perspective, various types of 3D assets produced by different 3D modeling software (such as Blender, Maya, 3ds Max, etc.) exhibit significant format discrepancies and lack of standardization. Specifically: (1) Inconsistent coordinate system definitions: Different software packages adopt varying coordinate system conventions (e.g., left-handed vs. right-handed systems, Y-up vs. Z-up, etc.), resulting in orientation errors or mirror flipping when assets are loaded in different environments; (2) Complex and diverse asset construction methods: Many assets employ multi-level node hierarchies, contain parent-child node scale inheritance relationships, and include hidden transformation matrices, which greatly increase the complexity of data processing.

Second, from a data quality perspective, the quality of various 3D assets is highly inconsistent, exhibiting significant heterogeneity. The main issues include: (1) Poor geometric quality: A large number of assets have overly simplified meshes with insufficient polygon counts, failing to accurately represent the detailed features of objects. Additionally, severe topological defects exist, such as non-manifold edges, self-intersecting faces, and isolated vertices. These problems render the assets unsuitable for tasks requiring watertight meshes (such as physical simulation, 3D printing, etc.); (2) Texture mapping errors: Some assets have serious UV unwrapping problems, with incorrect texture-to-geometry mapping, excessively low texture resolution, or missing textures, which compromise rendering quality.

Finally, from a data ecosystem perspective, existing datasets also suffer from the following systemic deficiencies: (1) Severely imbalanced category distribution: The datasets exhibit pronounced long-tail distribution characteristics, with abundant assets in common categories (such as chairs and tables), while assets in many rare categories that are important for real-world applications are extremely scarce, limiting the generalization capability of models; (2) Lack of structured information: The vast majority of assets are holistic, monolithic meshes, lacking hierarchical part decomposition and assembly relationship descriptions, which severely constrains the development of advanced applications such as fine-grained understanding, editable generation, and robotic manipulation.

To address the above issues, we first process and clean the raw 3D assets from the Objaverse series datasets through a combination of automated processing and manual assistance, obtaining a collection of high-quality static mesh processing results. We hope that researchers can conduct algorithmic exploration and research on a unified, high-quality benchmark. Second, we further perform part-level processing to obtain structured assets with consistent part-level decomposition, yielding a batch of high-quality original mesh segmentation results and individual part-level watertight meshes. We hope that researchers can further pursue more fine-grained algorithmic exploration and research. Finally, based on real-world object and product categories, we generate a collection of category-balanced 3D assets, aiming to help improve the generalization capability and algorithmic exploration of downstream tasks such as grasping.

\subsection{Existing Enhanced Objaverse Dataset}




Objaverse~\cite{objaverse} and Objaverse-XL~\cite{objaverseXL} provide the 3D research community with ultra-large-scale, diverse 3D asset datasets. However, researchers have been consistently challenged by issues of inconsistent data quality and complex 3D data processing workflows. Multiple subsequent works~\cite{lin2025objaverseplusplus, lu2025objaverseoa, jin2025canoobjdataset, qian2024objaversemix} have approached the filtering, processing, and enhancement of Objaverse from different perspectives.

From the perspective of data quality filtering, Objaverse++~\cite{lin2025objaverseplusplus} manually annotated 10,000 samples as training data based on key quality dimensions such as model transparency, single-object completeness, and scene attributes. Subsequently, a specialized quality assessment model was trained to ultimately filter out 500,000 high-quality samples.

From the perspective of geometric normalization, Objaverse-OA~\cite{lu2025objaverseoa} and Canonical Objaverse Dataset~\cite{jin2025canoobjdataset} addressed the critical issue of inconsistent 3D model orientations. Objaverse-OA established orientation normalization standards by annotating 14,000 orientation-aligned samples, while Canonical Objaverse Dataset utilized automated methods to annotate 32,000 samples.

From the perspective of data representation diversity, Objaverse-MIX~\cite{qian2024objaversemix} provided large-scale processing results containing 900,000 samples, offering multiple geometric representations such as point clouds, meshes, and voxels for each asset, accompanied by rendered images and text annotations, constructing a relatively complete training data asset package.

In summary, although existing works have improved Objaverse from different dimensions including quality filtering, orientation normalization, and multi-modal representation, the following systemic deficiencies still exist: (1) Insufficient comprehensiveness and depth in data processing, lacking a complete processing pipeline that covers format standardization, topology repair, high-quality rendering, and diverse sampling; (2) Filtered data still requires complex workflows before it can be used for training; (3) Processed data struggles to meet the training requirements of current 3D generation models due to issues such as fixed rendering viewpoints and single point cloud sampling strategy. In contrast, we employ a complete processing pipeline to curate high-quality data and process them into training-ready asset packages for researchers to use. Furthermore, we generate a collection of high-quality product assets as a supplement.


\subsection{Full-level Data Processing}
\begin{figure}[h]
    \centering
    \includegraphics[width=0.98\linewidth]{figures/data_processing_pipeline.png}
    \caption{Full-level Data Processing Pipeline.}
    \label{fig:full_level_data_pipeline}
\end{figure}

For full-level data, our processing pipeline consists primarily of three core steps: data rendering and format conversion, asset filtering, and post processing. Through this systematic processing workflow, we are able to obtain a collection of high-quality, training-ready data for static 3D generation networks. The overall processing pipeline is illustrated in Figure~\ref{fig:full_level_data_pipeline}, with each step carefully designed to ensure the quality and consistency of the output data.

\textbf{Data Rendering and Conversion.} Considering the diverse sources and varied formats of 3D assets in the original Objaverse dataset~\cite{objaverse,objaverseXL}, we first need to establish a unified data standard.
We combine manual annotation and automated conversion workflows to uniformly convert all 3D assets into single-frame static mesh representations with aligned orientations.
This standardization step is crucial for subsequent processing, as it eliminates coordinate system differences between different modeling software and excludes multi-view rendering inconsistencies caused by model animations. Subsequently, we use Blender as the rendering engine to perform multi-view rendering of each standardized static mesh. The rendering configuration includes two camera modes—orthographic projection and perspective projection—to cover different visual representation requirements. Finally, we uniformly export and store the processed static meshes in PLY format, which offers excellent cross-platform compatibility and efficient storage characteristics.

\textbf{Assets Filtering.} To ensure the high quality of training data, we establish a rigorous multi-dimensional filtering criteria. We comprehensively utilize the visual quality of rendering results and the geometric attributes of original 3D assets for data  filtering, primarily excluding the following three categories of inadequate data:
(1) Data with poor geometric quality. The original assets contain a large number of duplicated and overly simplified 3D assets. These assets typically exhibit: extremely low polygon counts, lack of necessary geometric details, and overly simple topological structures. We identify and exclude such assets by setting polygon count thresholds and calculating geometric complexity metrics. Retaining geometrically rich meshes with sufficient details can provide more valuable learning signals for the model.
(2) Data with poor texture quality. Texture quality directly affects the visual performance of rendering results. We exclude data with low image rendering quality due to the following reasons: serious UV mapping problems; overlapping faces in the geometry causing abnormal texture display; excessively low texture resolution or missing texture maps, etc.
(3) Data with large areas of thin structures. Thin structures pose special challenges in 3D generation tasks. We choose to exclude such data based on two main considerations: On one hand, from the perspective of implicit representations, the Signed Distance Field (SDF) at thin structures undergoes abrupt jumps, transitioning from positive to negative values within an extremely small spatial range, which significantly increases the difficulty of model learning and fitting and can easily lead to training instability; On the other hand, from the perspective of multi-view consistency, thin structures under certain viewpoints are difficult to observe or even completely invisible in 2D images (such as when viewing along the thin sheet direction), which reduces the stability and convergence speed of model learning. Therefore, excluding assets containing large areas of thin structures helps improve overall training effectiveness.





\textbf{Post Processing}.
After obtaining high-quality 3D assets, we further perform post-processing to generate training-ready data. The post-processing steps primarily include: watertight processing and point cloud sampling. (1) Watertight processing. Given an artist-created triangle mesh, we first compute the Unsigned Distance Field (UDF) on a uniform grid with $512^3$ resolution, and extract an $\epsilon$-contour thin shell mesh $\mathcal{M}$ using Marching Cubes with $\epsilon=1/512$. We then sample points on $\mathcal{M}$ and apply Delaunay triangulation to construct a volumetric tetrahedral mesh. Following the approach of ConvexMeshing~\cite{diazzi2021convexmeshing}, we optimize the tetrahedral cell labels (0 for inner, 1 for outer) using graph cut optimization, and extract the boundary surface as the final watertight mesh. (2) Point cloud sampling. Following the sampling strategies of Dora~\cite{chen2025dora} and Hunyuan3D 2.1~\cite{hunyuan3d2025hunyuan3d}, we implement a hybrid sampling scheme on watertight meshes by combining surface uniform sampling and edge importance sampling to ensure that the sampled point clouds can both adequately represent the overall geometric shape and accurately capture local detail features. It is worth noting that we rotated the coordinate system to Y-up during the post-processing stage.



\subsection{Part-level Data Processing}

\begin{figure}[h]
    \centering
    \includegraphics[width=0.98\linewidth]{figures/data_processing_pipeline_part.png}
    \caption{Part-level Data Processing Pipeline.}
    \label{fig:part_level_data_pipeline}
\end{figure}

For part-level data, we have designed a specialized data processing pipeline aimed at decomposing holistic static meshes into semantically consistent component collections. This pipeline consists primarily of three core steps: part splitting, asset filtering, and post-processing. Through this systematic processing workflow, we are able to transform original holistic static meshes into part-level components suitable for training part-aware generation networks. The overall processing pipeline is illustrated in Figure~\ref{fig:part_level_data_pipeline}.

\textbf{Part Splitting.} Part splitting is the critical step of breaking down holistic meshes into meaningful part units. We adopt a splitting strategy based on topological connectivity, first utilizing Connected Component Analysis to perform initial splitting of 3D assets, obtaining a collection of topologically independent original components. This step can automatically identify physically separated parts within the mesh, aligning the division of the holistic mesh with the semantic granularity designed by artists during the creation process.

After obtaining the initial decomposition results, we need to perform preliminary quality control filtering to exclude two types of extreme cases: (1) Complex assets with excessive components (component count $\textgreater$ 888): These assets typically contain numerous trivial small parts or decorative elements, whose excessive complexity significantly increases the difficulty of data processing; (2) Indivisible assets (component count $\textless$ 2): These assets cannot provide structural information at the part-level and do not meet the data requirements of part-aware generation tasks and are therefore excluded.

To address the over-fragmentation issue in the initial decomposition results, we further implement an automatic merging strategy. Specifically, we calculate the surface area of each original component and set area thresholds to identify small trivial parts. For components with areas significantly below the threshold, we merge them into adjacent larger components based on spatial adjacency relationships, thereby obtaining more reasonable part granularity. After this merging process, the final component count for the vast majority of assets is controlled between 10 and 40, a range that both retains sufficient semantic granularity and avoids excessive complexity, making it highly suitable for the training requirements of part-level generation tasks.

\textbf{Asset Filtering.} After completing part splitting, we establish a rigorous set of multi-dimensional filtering criteria to ensure that the retained data possesses both reasonable part-level structure and is suitable for model learning. The specific filtering rules are as follows: (1) Component quantity reasonableness verification. We exclude data with too few components ($\leq$1) or too many components ($\textgreater$50). Too few components indicate splitting failure or that the asset itself lacks structural complexity; too many components suggest that even after merging, the asset remains overly complex and may affect network learning. This filtering ensures that all assets in the dataset have moderate part-level complexity. (2) Part scale balance verification. We exclude data where the area of a single component exceeds 85\% of the total area of the surface of the object. These assets have extremely imbalanced part distributions, typically manifesting as one massive dominant part accompanied by several tiny auxiliary parts (such as a large tabletop with tiny leg connectors). This imbalanced part distribution is detrimental to the model learning reasonable proportional relationships and compositional logic among parts, and is therefore excluded. (3) Isolated small part quantity verification. We exclude data containing too many isolated small-area components. These isolated small parts are often decorative trivial elements that typically do not provide valuable semantic information and can interfere with the model's learning of relationships among major parts. By counting the proportion of isolated small parts, we can effectively identify and filter such low-quality data.

\textbf{Post Processing}. The post processing step aims to generate complete training data packages for each asset that passes the filtering. First, we perform systematic multi-view rendering of assets based on splitting results, generating two types of complementary image data: (1) RGB texture images: Rendered using original texture maps to obtain realistic appearance representations; (2) Part ID masks: Based on the splitting results, we assign a unique ID to each part and render 2D part mask images. In the mask images, each pixel's value corresponds to the ID of the part it belongs to. By simultaneously providing RGB images and part masks, this data can be used for training controllable part-aware object generation model. Subsequently, we perform watertight processing on the geometric data, separately processing the holistic mesh and individual part meshes: (1) Holistic mesh watertightening: We perform watertight processing on the merged complete object mesh to generate a topologically closed holistic representation; (2) Part mesh watertightening: We perform watertight processing on each independent part mesh separately, ensuring that each part is a topologically closed geometric entity. This step is crucial because many parts may have open boundaries at connection points after decomposition, and watertight processing can complete these boundaries, making each part an independent, complete 3D object.

Through the above complete processing pipeline, we ultimately obtain a high-quality part-level 3D dataset, with each sample containing: a reasonable number of semantically consistent parts, multi-view RGB images and part masks, and watertight holistic and part meshes. This rich data lays a solid foundation for training powerful part generation models, fine-grained 3D understanding or editing models, and simulation environments supporting complex robotic manipulation.

\subsection{Synthetic Data Generation}

\begin{figure}[h]
    \centering
    \includegraphics[width=0.8\linewidth]{figures/data_processing_pipeline_generated.png}
    \caption{Synthetic Data Generating Pipeline.}
    \label{fig:synthetic_data_pipeline}
\end{figure}

We leverage the powerful priors of generative models to synthesize data, aiming to bridge the significant gap in sample counts across object categories that exists in real-world datasets. To achieve this goal, our data synthesis pipeline consists of three main steps: text expansion, image generation, and 3D generation. The overall pipeline is illustrated in the Figure~\ref{fig:synthetic_data_pipeline}.

\textbf{Text Expansion}. We first collected and organized a complete e-commerce product category system from mainstream e-commerce platforms and product databases, constructing a category hierarchy that comprehensively covers real-world products. After excluding service-oriented virtual products (such as insurance, membership services.), we ultimately retained 1,252 specific physical product categories.

Using these product categories as semantic conditions, we employ an LLM model to generate detailed and diverse product descriptions. Our prompt design is centered around the following three points: (1) Ensuring basic rationality and authenticity, generating physically and logically reasonable descriptions around the category; (2) Providing rich visual details, including key attributes such as the object's shape, material, color, and size proportions; (3) Expanding diversity, imaginatively expanding the product's form, materials, and other content within a reasonable range, setting aside limitations of actual craftsmanship, cost, and other factors.


\textbf{Image Generation}. We select Qwen-Image to transform text descriptions into images. Although this model performs excellently in text understanding and image quality, as a general-purpose text-to-image model, it often generates images containing complex backgrounds, or viewpoints unsuitable for 3D generation. To ensure that the generated images are suitable for subsequent 3D generation step, we customize the model behavior through LoRA fine-tuning.

Specifically, our fine-tuning objective is to enable the model to generate images that meet the following quality standards: (1) Clean background: Solid color or simple gradient backgrounds with no complex scene elements, facilitating the separation of foreground objects; (2) Complete object: Ensuring that the overall geometric features can be accurately captured; (3) Appropriate position: The object is located at the image center, occupying a suitable proportion of the frame, avoiding being too large or too small; (4) Reasonable view point: Adopting three-quarter views or other information-rich observation angles that can simultaneously display multiple faces of the object, providing sufficient geometric cues for 3D generation; (5) Information-rich: Clearly displaying the object's key structural features, material properties, and detail elements.


\textbf{3D Generation}. We select the industry-leading HY3D-3.0 model~\cite{hunyuan3d_online} as our 3D generation engine. Leveraging the powerful capabilities of the HY3D-3.0 model, we are able to obtain high-quality 3D assets with the following characteristics: (1) Fine geometry: The generated meshes possess rich geometric details, accurately reconstructing the object's shape features, including complex structures such as edges, bumps, and holes; (2) Clear textures: Accurate texture mapping, with visual attributes such as color, material, and surface details highly consistent with the input image.


\subsection{Data Distribution and Visualization}





{\bf Full-level Data}. Using Objaverse and Objaverse-XL as base data sources, we conducted rigorous quality filtering and data processing workflows, ultimately curating 252,676 high-quality 3D assets for in-depth processing. These assets have undergone the complete data processing pipeline described above, ensuring that each asset meets training-ready standards.

To support model training and scientific evaluation, we perform a split of the dataset: 252,000 samples are allocated to the training set for comprehensive model learning; 276 samples are allocated to the validation set for hyperparameter tuning and model selection during training; and 400 samples are allocated to the test set for final model performance evaluation and benchmarking.

In terms of category coverage, the entire dataset spans 19 top-level categories, further subdivided into 74 mid-level subcategories, and ultimately contains 389 fine-grained classifications, such as Animal-Virtual/Extinct Animals-Anthropomorphic Animals, Weapon-Firearms-Guns.

\begin{figure}[h]
    \centering
    \includegraphics[width=0.9\linewidth]{figures/full_static1.png}
    \caption{The Top-level Category Distribution of Full-level Data.}
    \label{fig:top_level_distribution_full_data}
\end{figure}

\begin{figure}[h]
    \centering
    \includegraphics[width=0.82\linewidth]{figures/full_data_vis.png}
    \caption{Visualization of the full-level dataset, including sharp edge point clouds, random surface point clouds, watertight meshes, and rendered images.}
    \label{fig:full_data_vis}
\end{figure}



{\bf Part-level Data}. The part-level dataset comprises 240,524 samples in total, with a mean component count of 14.13 and a median of 11, exhibiting a diverse distribution of component complexity. Specifically, 24.63\% of samples contain 2-5 components, representing relatively simple object structures; 24.83\% of samples contain 6-10 components, covering objects with moderate structural complexity; 27.00\% of samples contain 11-20 components, encompassing more intricate assemblies; and the remaining samples contain 21-50 components, representing highly complex multi-part objects. The detailed statistical distribution of component counts is illustrated in Fig.~\ref{fig:component_distribution_part_data}.

\begin{figure}[h]
    \centering
    \includegraphics[width=0.95\linewidth]{figures/part_static.png}
    \caption{The Component Distribution of Part-level Data.The prominent peaks at 16, 34, and 35 primarily stem from humanoid models that share identical geometric structures but differ in texture. Considering that various research scenarios and application needs may require such texture variant data, we chose to retain this portion of the data without deduplication.}
    \label{fig:component_distribution_part_data}
\end{figure}

\begin{figure}[h]
    \centering
    \includegraphics[width=0.95\linewidth]{figures/part_data_vis1.png}
    \caption{Part-level dataset visualization, showing individual components and the assembled model color-coded by component ID.}
    \label{fig:full_data_vis}
\end{figure}




{\bf Synthetic Data}. The Synthetic Data contains more than 125k samples. The category system design of this dataset fully considers the needs of real-world applications, ultimately encompassing 20 top-level categories, 130 mid-level subcategories, and 1,252 fine-grained classifications of product data. The breadth and depth of this category system far exceed existing real datasets, with coverage ranging from daily necessities and consumer electronics to professional industrial products.

\begin{figure}[h]
    \centering
    \includegraphics[width=0.95\linewidth]{figures/gen_static.png}
    \caption{The Top-level Category Distribution of Synthetic Data.}
    \label{fig:component_distribution_gen_data}
\end{figure}

\begin{figure}[h]
    \centering
    \includegraphics[width=0.95\linewidth]{figures/gen_data_vis.png}
    \caption{Synthetic dataset visualization, showing diverse samples from 5 fine-grained categories.}
    \label{fig:full_data_vis}
\end{figure}





\section{Evaluation}

\subsection{Implementation Details}
To validate the effectiveness of Full-level Data in 3D generation tasks, we use Hunyuan3D-2.1 as our baseline. While maintaining the core architectural design principles, we appropriately scale down the model to reduce training costs and train a lightweight Hunyuan3D-2.1-Small model. For evaluation, we use ULIP~\cite{xue2023ulip} and Uni3D~\cite{zhou2023uni3d} to measure the consistency between images and generated meshes.

\textbf{Model Architecture Adjustments}. Compared to the original Hunyuan3D-2.1 model, our Small model incorporates the following key architectural modifications to balance model capacity with training efficiency: (1) Channel dimension reduction: We reduce the base channel dimension from 2048 to 1536. (2) Architecture simplification: We remove the Mixture of Experts (MoE) structure and adopt a fully Dense architecture instead. After these adjustments, our Hunyuan3D-2.1-Small model contains 832M parameters.

\textbf{Progressive Training Strategy}. Drawing on the successful experience of Hunyuan3D-2.1, we employ a progressive token resolution training strategy, starting from 512 tokens and gradually increasing the token count to improve representation fidelity, ultimately reaching 4096 tokens. Detailed training configurations are provided in Table~\ref{tab:full_level_data_train}.

\begin{table}[h]
    \centering
    \begin{tabular}{c||c|c|c|c}
    \hline
         Tokens &  Batch size & Image Size & Learning rate & Traning steps \\
    \hline
         512 & 512 & 224 & 1.e-4 & 800k \\
         2048 & 256 & 224 & 5.e-5 & 400k \\
         2048 & 256 & 518 & 5.e-5 & 200k \\
         4096 & 128 & 518 & 1.e-5 & 400k \\
    \hline
    \end{tabular}
    \caption{Hunyuan3D-2.1-Small Training Strategy.}
    \label{tab:full_level_data_train}
\end{table}

\subsection{Experimental Results}

To comprehensively evaluate the effectiveness of our full-level dataset, we conducted comparative experiments with several representative state-of-the-art open-source methods, including Michelangelo~\cite{zhao2024michelangelo}, Craftsman~\cite{li2024craftsman}, Trellis~\cite{xiang2024structured}, and Hunyuan3D 2.1~\cite{hunyuan3d2025hunyuan3d}. These baseline methods have all demonstrated outstanding performance in the field of 3D generation. As shown in Table~\ref{tab:full_level_data_eval} and Figure~\ref{fig:full_level_data_eval}, despite having significantly fewer parameters than Trellis and Hunyuan3D 2.1, our model achieves comparable generation quality when trained on our open-sourced dataset, while outperforming the similarly-sized Craftsman. This experimental result fully demonstrates the high-quality characteristics of our open-sourced dataset. Meanwhile, this also indicates that data quality plays a crucial role in 3D generation tasks. The dataset we have constructed can provide the community with an efficient training resource, enabling researchers to focus more on algorithm innovation and model optimization rather than tedious data processing and preparation work.

\begin{table}[h]
    \centering
    \begin{tabular}{c|c|c|c|c}
    \hline
         Methods &  Token length & Model Size (M) & Uni3D-I $\uparrow$ & ULIP-I $\uparrow$ \\
    \hline
         Michelangelo~\cite{zhao2024michelangelo} & 257 & 105 & 0.3169 & 0.2186 \\
         CraftsMan~\cite{li2024craftsman} & 2048 & 852 & 0.3351 & 0.2264 \\
         Trellis~\cite{xiang2024structured} & 10000* & 1156 & 0.3641 & 0.2454 \\
         Hunyuan3D 2.1~\cite{hunyuan3d2025hunyuan3d} & 4096 & 1238 & 0.3636 & 0.2446 \\
         Ours  & 4096 & 832 & 0.3606 & 0.2424 \\
    \hline
    \end{tabular}
    \caption{The quantitative comparison for image-to-3D generation on our test dataset.``*'' denotes the average token length for active voxel.}
    \label{tab:full_level_data_eval}
\end{table}

\begin{figure}[h]
    \centering
    \includegraphics[width=0.95\linewidth]{figures/eval_full.png}
    \caption{The qualitative comparison for image-to-3D generation on our test dataset.}
    \label{fig:full_level_data_eval}
\end{figure}


\section{Conclusion}
In this work, we present HY3D-Bench, an open-source ecosystem designed to surmount the data processing bottlenecks currently constraining 3D generative models. We establish a unified foundation through three key contributions. First, we curate a high-fidelity library of 252k 3D objects derived from large-scale repositories such as Objaverse and Objaverse-XL. We employ a rigorous, multi-stage pipeline to ensure training readiness, producing essential artifacts such as watertight meshes and multi-view renderings. Second, we introduce 240k structured part-level decomposition, providing the granularity essential for advancing fine-grained perception, part-aware generation, and controllable 3D editing. Third, to mitigate real-world data distribution gaps, we develop a scalable AIGC-driven synthesis pipeline, contributing 125k synthetic assets to enrich diversity within long-tail categories. Empirical validation using the Hunyuan3D-2.1-Small model confirms the practical utility of our dataset. By democratizing access to these resources, HY3D-Bench aims to catalyze innovation across 3D perception, robotics, and digital content creation. Future efforts will focus on extending this framework to include dynamic assets and broader tasks.



\clearpage


\section{Contributors}
\large{Authors are listed \textbf{alphabetically by the first name}.}
\definecolor{tencentblue}{RGB}{38,54,221}
\large{
\color{tencentblue}
\begin{multicols}{2}
\raggedcolumns
Bowen Zhang\\
Chunchao Guo\\
Dongyuan Guo\\
Haolin Liu\\
Hongyu Yan\\
Huiwen Shi\\
Jiaao Yu\\
Jiachen Xu\\
Jingwei Huang\\
Kunhong Li\\
Lifu Wang\\
Linus\\
Penghao Wang\\
Qingxiang Lin\\
Ruining Tang\\
Xianghui Yang\\
Yang Li\\
Yunfei Zhao\\
Yunhan Yang\\
Zeqiang Lai\\
Zhihao Liang\\
Zibo Zhao\\
\end{multicols}}

\large{Other contributors are listed \textbf{alphabetically by the first name}.}
\definecolor{tencentblue}{RGB}{38,54,221}
\large{
\color{tencentblue}
\begin{multicols}{2}
\raggedcolumns
Chao Zhang\\
Edwarrd Wang\\
Hao Zhang\\
Jiaxin Lin\\
Peng He\\
Yirui Guan\\
Yonghao Tan\\
Zheng Ye\\
\end{multicols}}

\clearpage

\bibliography{colm2024_conference}
\bibliographystyle{colm2024_conference}


\end{document}

