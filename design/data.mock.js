// Brain University — mock data layer
// Mirrors the contract from agents/ + graph/ in the Python codebase.
// Cross-disciplinary: Aero, CS, Math, Bio, Systems.

window.BU_DATA = (() => {

  // ─── Clusters (= courses, Louvain communities) ──────────────────────
  const CLUSTERS = [
    { id: 0, name: "Aerodynamics & Flight",  color: "#7641eb", emoji: "🛩",
      blurb: "Lift, drag, compressible flow, control authority." },
    { id: 1, name: "Algorithms & Computation", color: "#2ec4b6", emoji: "⌬",
      blurb: "Search, optimization, graph theory, complexity." },
    { id: 2, name: "Differential Geometry",  color: "#f59e0b", emoji: "∮",
      blurb: "Manifolds, curvature, the language of physics." },
    { id: 3, name: "Systems & Control",      color: "#1e6fa8", emoji: "⚙",
      blurb: "Feedback, stability, observer design, MPC." },
    { id: 4, name: "Cellular Biology",       color: "#84cc16", emoji: "✺",
      blurb: "Membranes, signaling, the stochastic engine of life." },
    { id: 5, name: "Information Theory",     color: "#c5a3ff", emoji: "Φ",
      blurb: "Entropy, channel capacity, compression." },
  ];

  // ─── Concepts (~60, distributed across clusters) ────────────────────
  // Edges encode prerequisites + cross-cluster bridges.
  const NODES = [
    // 0 — Aerodynamics
    { id: "Reynolds_number",        cluster: 0, degree: 14, name: "Reynolds number", para: "A" },
    { id: "Bernoulli",              cluster: 0, degree: 9,  name: "Bernoulli's principle", para: "A" },
    { id: "Boundary_layer",         cluster: 0, degree: 11, name: "Boundary layer", para: "A" },
    { id: "Navier_Stokes",          cluster: 0, degree: 18, name: "Navier–Stokes equations", para: "P" },
    { id: "Compressible_flow",      cluster: 0, degree: 8,  name: "Compressible flow" },
    { id: "Lift_coefficient",       cluster: 0, degree: 7,  name: "Lift coefficient" },
    { id: "Vortex_shedding",        cluster: 0, degree: 6,  name: "Vortex shedding" },
    { id: "Mach_number",            cluster: 0, degree: 5,  name: "Mach number" },
    { id: "Drag_polar",             cluster: 0, degree: 4,  name: "Drag polar" },

    // 1 — Algorithms
    { id: "Dijkstra",               cluster: 1, degree: 13, name: "Dijkstra's algorithm" },
    { id: "BFS",                    cluster: 1, degree: 9,  name: "Breadth-first search" },
    { id: "DFS",                    cluster: 1, degree: 8,  name: "Depth-first search" },
    { id: "Graph_theory",           cluster: 1, degree: 16, name: "Graph theory", para: "A" },
    { id: "Dynamic_programming",    cluster: 1, degree: 11, name: "Dynamic programming" },
    { id: "PageRank",               cluster: 1, degree: 10, name: "PageRank" },
    { id: "Louvain_clustering",     cluster: 1, degree: 7,  name: "Louvain clustering" },
    { id: "A_star",                 cluster: 1, degree: 8,  name: "A* search" },
    { id: "Complexity_classes",     cluster: 1, degree: 6,  name: "Complexity classes" },

    // 2 — Differential geometry
    { id: "Manifold",               cluster: 2, degree: 12, name: "Manifold", para: "A" },
    { id: "Tensor",                 cluster: 2, degree: 10, name: "Tensor" },
    { id: "Curvature",              cluster: 2, degree: 9,  name: "Curvature" },
    { id: "Riemannian_metric",      cluster: 2, degree: 8,  name: "Riemannian metric" },
    { id: "Geodesic",               cluster: 2, degree: 7,  name: "Geodesic" },
    { id: "Lie_group",              cluster: 2, degree: 6,  name: "Lie group" },
    { id: "Differential_form",      cluster: 2, degree: 5,  name: "Differential form" },
    { id: "Stokes_theorem",         cluster: 2, degree: 6,  name: "Stokes' theorem" },

    // 3 — Systems & control
    { id: "Kalman_filter",          cluster: 3, degree: 13, name: "Kalman filter", para: "P" },
    { id: "PID_control",            cluster: 3, degree: 9,  name: "PID control" },
    { id: "Lyapunov_stability",     cluster: 3, degree: 11, name: "Lyapunov stability" },
    { id: "State_space",            cluster: 3, degree: 12, name: "State-space model" },
    { id: "Observability",          cluster: 3, degree: 7,  name: "Observability" },
    { id: "MPC",                    cluster: 3, degree: 8,  name: "Model-predictive control" },
    { id: "Bode_plot",              cluster: 3, degree: 5,  name: "Bode plot" },
    { id: "Transfer_function",      cluster: 3, degree: 7,  name: "Transfer function" },

    // 4 — Cell biology
    { id: "Action_potential",       cluster: 4, degree: 11, name: "Action potential" },
    { id: "Ion_channel",            cluster: 4, degree: 9,  name: "Ion channel" },
    { id: "Membrane_potential",     cluster: 4, degree: 10, name: "Membrane potential" },
    { id: "Hodgkin_Huxley",         cluster: 4, degree: 8,  name: "Hodgkin–Huxley model" },
    { id: "Synaptic_plasticity",    cluster: 4, degree: 7,  name: "Synaptic plasticity" },
    { id: "Diffusion",              cluster: 4, degree: 9,  name: "Diffusion" },
    { id: "Stochastic_gene_expression", cluster: 4, degree: 6, name: "Stochastic gene expression" },

    // 5 — Information theory
    { id: "Shannon_entropy",        cluster: 5, degree: 14, name: "Shannon entropy", para: "A" },
    { id: "Mutual_information",     cluster: 5, degree: 10, name: "Mutual information" },
    { id: "Channel_capacity",       cluster: 5, degree: 9,  name: "Channel capacity" },
    { id: "KL_divergence",          cluster: 5, degree: 11, name: "KL divergence" },
    { id: "Source_coding",          cluster: 5, degree: 6,  name: "Source coding" },
    { id: "Markov_chain",           cluster: 5, degree: 12, name: "Markov chain" },
    { id: "Rate_distortion",        cluster: 5, degree: 5,  name: "Rate–distortion theory" },
  ];

  // Edges — within-cluster prereqs + cross-cluster bridges.
  const EDGES = [
    // Aero
    ["Bernoulli","Lift_coefficient"], ["Bernoulli","Boundary_layer"],
    ["Boundary_layer","Reynolds_number"], ["Reynolds_number","Navier_Stokes"],
    ["Navier_Stokes","Compressible_flow"], ["Compressible_flow","Mach_number"],
    ["Mach_number","Drag_polar"], ["Boundary_layer","Vortex_shedding"],
    ["Lift_coefficient","Drag_polar"], ["Reynolds_number","Vortex_shedding"],
    ["Navier_Stokes","Boundary_layer"], ["Bernoulli","Reynolds_number"],

    // Algorithms
    ["BFS","Graph_theory"], ["DFS","Graph_theory"], ["Dijkstra","Graph_theory"],
    ["A_star","Dijkstra"], ["A_star","Graph_theory"],
    ["Dynamic_programming","Dijkstra"], ["PageRank","Graph_theory"],
    ["Louvain_clustering","Graph_theory"], ["Complexity_classes","Dynamic_programming"],
    ["BFS","DFS"],

    // Diff geo
    ["Manifold","Tensor"], ["Manifold","Curvature"], ["Manifold","Riemannian_metric"],
    ["Riemannian_metric","Geodesic"], ["Curvature","Riemannian_metric"],
    ["Lie_group","Manifold"], ["Differential_form","Stokes_theorem"],
    ["Tensor","Curvature"], ["Differential_form","Manifold"],

    // Control
    ["State_space","Kalman_filter"], ["State_space","Observability"],
    ["State_space","MPC"], ["Lyapunov_stability","State_space"],
    ["PID_control","Transfer_function"], ["Transfer_function","Bode_plot"],
    ["MPC","Lyapunov_stability"], ["Kalman_filter","Observability"],

    // Bio
    ["Membrane_potential","Action_potential"], ["Ion_channel","Membrane_potential"],
    ["Action_potential","Hodgkin_Huxley"], ["Ion_channel","Action_potential"],
    ["Synaptic_plasticity","Action_potential"], ["Diffusion","Membrane_potential"],
    ["Stochastic_gene_expression","Diffusion"],

    // Info
    ["Shannon_entropy","Mutual_information"], ["Shannon_entropy","Channel_capacity"],
    ["Mutual_information","KL_divergence"], ["KL_divergence","Source_coding"],
    ["Markov_chain","Shannon_entropy"], ["Channel_capacity","Rate_distortion"],
    ["Markov_chain","KL_divergence"],

    // ── Cross-cluster bridges (the magic) ──
    ["Reynolds_number","Navier_Stokes"], // self
    ["Navier_Stokes","Manifold"],            // aero ↔ diff geo
    ["Curvature","Vortex_shedding"],         // diff geo ↔ aero
    ["Graph_theory","Markov_chain"],         // algo ↔ info
    ["PageRank","Markov_chain"],             // algo ↔ info
    ["Dijkstra","A_star"],
    ["State_space","Manifold"],              // control ↔ diff geo
    ["Kalman_filter","Markov_chain"],        // control ↔ info
    ["Hodgkin_Huxley","State_space"],        // bio ↔ control
    ["Hodgkin_Huxley","Diffusion"],
    ["Diffusion","Navier_Stokes"],           // bio ↔ aero
    ["Synaptic_plasticity","Mutual_information"], // bio ↔ info
    ["Stochastic_gene_expression","Markov_chain"],// bio ↔ info
    ["Louvain_clustering","Graph_theory"],
    ["Lyapunov_stability","Manifold"],       // control ↔ diff geo
    ["Lie_group","State_space"],             // diff geo ↔ control
    ["Tensor","Riemannian_metric"],
    ["Geodesic","A_star"],                   // diff geo ↔ algo
    ["Rate_distortion","Channel_capacity"],
  ];

  // Bridge nodes — appear in `bridges` of each cluster
  const BRIDGE_PAIRS = {
    Navier_Stokes: [2],
    Vortex_shedding: [2],
    Diffusion: [0, 5],
    Markov_chain: [1, 3, 4],
    PageRank: [5],
    State_space: [2, 4],
    Kalman_filter: [5],
    Hodgkin_Huxley: [3],
    Synaptic_plasticity: [5],
    Manifold: [0, 3],
    Lie_group: [3],
    Geodesic: [1],
    Curvature: [0],
  };

  // ─── Lessons (auto-generated mock content) ──────────────────────────
  const LESSONS = {
    Reynolds_number: {
      title: "Reynolds number",
      summary: "A dimensionless ratio that says when a flow stops behaving like honey and starts behaving like a thunderstorm. Inertial forces over viscous forces — Re = ρuL/μ. Below ~2300 in a pipe: laminar, predictable, reversible. Above ~4000: turbulent, chaotic, governed by statistics not trajectories.",
      key_ideas: [
        { h: "It's a regime selector.", b: "Same fluid, same geometry — change Re by 10× and the equations you reach for change. Below the transition, you can integrate. Above it, you simulate or measure." },
        { h: "It rescales experiments.", b: "Match Re between a wind-tunnel model and the full-scale aircraft and the dimensionless flow fields are the same. This is why we can test a 1:50 model and trust the numbers." },
        { h: "Universal across scales.", b: "From swimming bacteria (Re ≈ 10⁻⁴) to a 747 wing (Re ≈ 10⁷) — eleven decades. The same dimensionless group governs all of them." },
      ],
      worked_example: "747 cruise: ρ ≈ 0.38 kg/m³ at 35,000 ft, u ≈ 250 m/s, chord L ≈ 8 m, μ ≈ 1.5×10⁻⁵ Pa·s. Re = (0.38 × 250 × 8) / 1.5×10⁻⁵ ≈ 5.1×10⁷. Deeply turbulent. The boundary layer transitions within the first ~5% of chord.",
      evidence: ["wiki/Reynolds_number", "arxiv/physics.flu-dyn/1903.07921", "Schlichting §1.3"],
      quiz: [{
        q: "A submarine moves at 5 m/s. The flow Reynolds number is most useful for predicting:",
        choices: ["Buoyancy", "Whether the boundary layer is laminar or turbulent", "Total drag in absolute units", "Wave height at the surface"],
        correct: 1,
        why: "Re sets the regime — laminar vs turbulent — which dictates the model you use to compute drag. It doesn't give you the drag itself."
      }],
    },
    Navier_Stokes: {
      title: "Navier–Stokes equations",
      summary: "The full statement of momentum conservation for a viscous fluid. Beautiful, complete, and — for the general 3D case — still has no proof of smooth solutions for all time. A Clay Millennium Prize sits on it.",
      key_ideas: [
        { h: "Three force balances.", b: "Inertia = pressure gradient + viscous diffusion + body forces. Every term has a clear physical referent — that's why the equation has survived 200 years." },
        { h: "Linear in the wrong place.", b: "The convective term (u·∇)u is the source of all nonlinearity, all turbulence, all the trouble." },
        { h: "Limits give you everything.", b: "Take Re→∞: Euler. Re→0: Stokes. Incompressible: ∇·u=0. Each special case is a course of its own." },
      ],
      worked_example: "Pipe flow, steady, fully-developed, axisymmetric. The equation collapses to dp/dz = μ ∇²u_z. Solving with no-slip at the wall yields the Hagen–Poiseuille parabolic profile and a flow rate Q = πR⁴Δp / 8μL.",
      evidence: ["wiki/Navier_Stokes_equations", "arxiv/math.AP/0711.3203", "Batchelor §3.1"],
      quiz: [{
        q: "The convective term (u·∇)u is responsible for:",
        choices: ["Conservation of mass", "Linear superposition of solutions", "Turbulence and nonlinear instability", "Pressure smoothing"],
        correct: 2, why: "(u·∇)u is the only nonlinear term in the incompressible NS equations and the source of cascade dynamics."
      }],
    },
    Manifold: {
      title: "Manifold",
      summary: "A space that locally looks Euclidean but globally need not be. The earth's surface is a 2-manifold: zoom in and you see a flat plane, zoom out and you see a sphere. Modern physics treats spacetime as a 4-manifold; control theory treats robot configuration spaces as manifolds.",
      key_ideas: [
        { h: "Charts and atlases.", b: "Cover the manifold with overlapping coordinate patches. On overlaps, the transition map between two charts must be smooth. The manifold is the equivalence class of atlases — it doesn't depend on which one you pick." },
        { h: "Tangent space at a point.", b: "At every point p there's a vector space T_pM of velocities through p. This is where derivatives live." },
        { h: "Why it matters for control.", b: "A drone's orientation lives on SO(3), not ℝ³. Pretending it's ℝ³ gives you gimbal lock and singularities. Treating it as a manifold gives you Lie-algebra control laws that work everywhere." },
      ],
      worked_example: "S² (the unit sphere). Two charts: stereographic projection from the north pole (covers everywhere except N) and from the south pole (everywhere except S). On the overlap, the transition map is z↦1/z̄ — smooth. So S² is a smooth 2-manifold.",
      evidence: ["wiki/Manifold", "arxiv/math.DG/0506395", "Lee, Smooth Manifolds, Ch. 1"],
      quiz: [{
        q: "Why model a quadrotor's orientation as SO(3) instead of three Euler angles?",
        choices: ["SO(3) is faster to compute", "Euler angles have singularities; SO(3) doesn't", "SO(3) uses fewer parameters", "Euler angles are non-differentiable"],
        correct: 1, why: "Euler angles parameterize SO(3) but introduce singularities (gimbal lock). Working on the manifold avoids them."
      }],
    },
    Markov_chain: {
      title: "Markov chain",
      summary: "A stochastic process where the future depends on the present and not the past. P(X_{t+1}|X_t,X_{t-1},…) = P(X_{t+1}|X_t). One assumption — memorylessness — and you unlock half of probability theory.",
      key_ideas: [
        { h: "The transition matrix is the model.", b: "An n×n stochastic matrix P with rows summing to 1. P^k gives the k-step distribution. Eigenvalues control mixing." },
        { h: "Stationary distribution.", b: "If the chain is irreducible and aperiodic, π = πP exists and is unique. PageRank is exactly this — the stationary distribution of a random walk on the web." },
        { h: "The bridge to physics and biology.", b: "Hidden Markov Models, Markov Chain Monte Carlo, ion-channel gating, language models — same machinery, different domain vocabulary." },
      ],
      worked_example: "A two-state weather chain: P(rain→rain)=0.7, P(rain→sun)=0.3, P(sun→rain)=0.4, P(sun→sun)=0.6. Stationary distribution: π_rain = 4/7, π_sun = 3/7. Long-run fraction of rainy days ≈ 57%.",
      evidence: ["wiki/Markov_chain", "arxiv/math.PR/1304.3252", "Norris §1.5"],
      quiz: [{
        q: "PageRank can be interpreted as:",
        choices: ["A shortest-path algorithm", "The stationary distribution of a random walk on the link graph", "A clustering of pages", "An entropy estimate"],
        correct: 1, why: "PageRank ranks pages by π_i, the probability of being at page i in the stationary distribution of a damped random walk."
      }],
    },
    State_space: {
      title: "State-space model",
      summary: "Replace high-order ODEs with first-order vector equations. ẋ = Ax + Bu, y = Cx + Du. Now everything is linear algebra: stability is eigenvalues, controllability is a rank, observability is a rank. The whole subject becomes geometric.",
      key_ideas: [
        { h: "State = minimum information.", b: "x_t is whatever you must know now to predict the future given the input. For a mass-spring-damper, that's position and velocity — two numbers, two state variables." },
        { h: "A is the autonomy.", b: "Eigenvalues of A live in the complex plane. Left half = stable, right half = unstable, imaginary axis = oscillation. The whole picture in one matrix." },
        { h: "B and C are the conversation.", b: "B says how inputs enter the state. C says what part of the state is visible at the output. Mismatched B and C give uncontrollable or unobservable modes — the silent killers of feedback design." },
      ],
      worked_example: "Pendulum, small-angle: ẍ = -(g/L)x. State x=[θ, θ̇]ᵀ, ẋ = [[0,1],[-g/L,0]]x. Eigenvalues ±i√(g/L) — pure oscillation, neutrally stable, exactly what we'd expect.",
      evidence: ["wiki/State-space_representation", "Astrom & Murray Ch. 5", "arxiv/eess.SY/2104.11122"],
      quiz: [{
        q: "Eigenvalues of A all in the open left half-plane means:",
        choices: ["Controllable", "Observable", "Asymptotically stable", "Minimum phase"],
        correct: 2, why: "Real parts < 0 ⇒ all modes decay ⇒ asymptotic stability of the autonomous system ẋ = Ax."
      }],
    },
    Kalman_filter: {
      title: "Kalman filter",
      summary: "The optimal recursive estimator for linear-Gaussian systems. You start with a guess and a covariance, you predict ahead through the dynamics, you correct using a measurement weighted by how trustworthy it is. Two equations, infinite applications — from Apollo to your phone's GPS.",
      key_ideas: [
        { h: "Two steps, every tick.", b: "Predict: x̂ = Ax̂_prev, P = APAᵀ + Q. Update: K = PCᵀ(CPCᵀ + R)⁻¹, x̂ ← x̂ + K(y − Cx̂)." },
        { h: "K is a trust ratio.", b: "When R (measurement noise) is huge, K is tiny — ignore the sensor. When Q (process noise) is huge, K is near 1 — trust the sensor." },
        { h: "The covariance is the value.", b: "P tells you how much you know. It's not just an output, it's the whole point — it's how the filter knows when to ask for more data." },
      ],
      worked_example: "1D position tracking with noisy GPS. After enough steps, P converges to a fixed point determined by Q and R only — independent of initial uncertainty. The filter forgets bad starts.",
      evidence: ["wiki/Kalman_filter", "Kalman 1960 (original)", "arxiv/eess.SY/2007.04357"],
      quiz: [{
        q: "If the measurement noise covariance R grows very large, the Kalman gain K:",
        choices: ["Grows toward 1", "Stays the same", "Shrinks toward 0", "Becomes negative"],
        correct: 2, why: "Large R means untrustworthy measurements; K shrinks so the update barely uses them, and the filter relies on the prediction."
      }],
    },
  };

  // For nodes without authored lessons — generate a passable placeholder.
  function lessonFor(nodeId) {
    if (LESSONS[nodeId]) return LESSONS[nodeId];
    const node = NODES.find(n => n.id === nodeId);
    if (!node) return null;
    const cluster = CLUSTERS[node.cluster];
    return {
      title: node.name,
      summary: `${node.name} sits inside the ${cluster.name} course. ${cluster.blurb} This concept is connected to ${node.degree} others, making it a ${node.degree > 9 ? "hub" : "supporting"} node in its course.`,
      key_ideas: [
        { h: "Why it matters.", b: `${node.name} appears in arguments across ${node.degree} other concepts, so it's a high-leverage place to spend reading time.` },
        { h: "What to read first.", b: `Start with the wiki page, then the canonical paper. Do the worked example before the proofs.` },
        { h: "Where it goes next.", b: `From here, the natural deepening is into adjacent concepts in ${cluster.name}, with bridges to other courses through shared bridge nodes.` },
      ],
      worked_example: "(Auto-generated lesson — full Claude rich-mode lesson available with API key.)",
      evidence: [`wiki/${node.id}`],
      quiz: [{
        q: `Which of these is the strongest reason ${node.name} matters?`,
        choices: ["It's required by exam syllabus", "It's a hub concept connected to many others", "It's the easiest topic", "It's the newest"],
        correct: 1, why: "Hub status is what the foundation-scoring algorithm uses to pick starting points."
      }],
    };
  }

  // ─── Tour planner — 6 stops with rationales ────────────────────────
  // Mirrors agents/lesson_plan.py: start → deepen 2× → bridge → deepen 1–2× → capstone.
  const TOURS = {
    // Tour starting from Reynolds number — the canonical demo path.
    Reynolds_number: [
      { node: "Reynolds_number",  cluster: 0, kind: "start",
        rationale: "Highest centrality node in Aerodynamics (degree 14, spans 2 courses). The dimensionless ratio that tells you which equations to reach for." },
      { node: "Boundary_layer",   cluster: 0, kind: "deepen",
        rationale: "Direct prerequisite. Re only matters because of what happens in the thin viscous layer near the wall — this is where regime selection actually plays out." },
      { node: "Navier_Stokes",    cluster: 0, kind: "deepen",
        rationale: "The full equation Re is a dimensionless ratio of. Going up the abstraction ladder so the regime question becomes obvious from the structure." },
      { node: "Manifold",         cluster: 2, kind: "bridge",
        rationale: "Bridge to Differential Geometry. Modern fluid dynamics treats the flow as a section of a tensor bundle on a 4-manifold. This is where physics and geometry meet." },
      { node: "Tensor",           cluster: 2, kind: "deepen",
        rationale: "The viscous stress tensor that appears in NS is a tensor field. Now you have the language to write the equation properly." },
      { node: "Markov_chain",     cluster: 5, kind: "capstone",
        rationale: "Capstone: turbulent flow above the critical Re is governed by statistics, not trajectories. The connection to Markov chains and information theory closes the loop — a single concept opens onto a whole landscape." },
    ],
  };

  function planTour(startId) {
    if (TOURS[startId]) return TOURS[startId];
    // Fallback: greedy traversal — start, two highest-degree neighbors, one bridge, one more, capstone.
    const start = NODES.find(n => n.id === startId);
    if (!start) return null;
    const adj = adjacencyOf(startId);
    const inCluster = adj.filter(n => n.cluster === start.cluster).sort((a,b)=>b.degree-a.degree);
    const bridges = adj.filter(n => n.cluster !== start.cluster);
    const out = [{
      node: startId, cluster: start.cluster, kind: "start",
      rationale: `Selected for centrality — degree ${start.degree}, in ${CLUSTERS[start.cluster].name}.`
    }];
    if (inCluster[0]) out.push({ node: inCluster[0].id, cluster: inCluster[0].cluster, kind: "deepen", rationale: `Deepening into ${CLUSTERS[start.cluster].name} via the strongest local prerequisite.` });
    if (inCluster[1]) out.push({ node: inCluster[1].id, cluster: inCluster[1].cluster, kind: "deepen", rationale: `One more depth-step inside the same course before crossing.` });
    if (bridges[0]) out.push({ node: bridges[0].id, cluster: bridges[0].cluster, kind: "bridge", rationale: `Bridge to ${CLUSTERS[bridges[0].cluster].name} — the connection runs through this concept.` });
    if (inCluster[2]) out.push({ node: inCluster[2].id, cluster: inCluster[2].cluster, kind: "deepen", rationale: `Returning to the home course to consolidate.` });
    out.push({ node: "Markov_chain", cluster: 5, kind: "capstone", rationale: `Capstone: tying the journey to a statistical worldview.` });
    return out;
  }

  function adjacencyOf(nodeId) {
    const ids = new Set();
    for (const [a,b] of EDGES) {
      if (a === nodeId) ids.add(b);
      if (b === nodeId) ids.add(a);
    }
    return [...ids].map(id => NODES.find(n => n.id === id)).filter(Boolean);
  }

  // ─── Foundation picks (Start here cards) ───────────────────────────
  const FOUNDATION_PICKS = [
    {
      raw: "Reynolds_number", name: "Reynolds number", cluster: 0, score: 0.94,
      rationale: "Top of the foundation index. Bridges to differential geometry, used downstream by 14 other concepts.",
      metrics: { degree: 14, span: 2, size: 9, hasWiki: true, rl: 0.32 },
    },
    {
      raw: "Markov_chain", name: "Markov chain", cluster: 5, score: 0.91,
      rationale: "Spans 4 courses — the connective tissue between algorithms, control, biology, and information theory.",
      metrics: { degree: 12, span: 4, size: 7, hasWiki: true, rl: 0.28 },
    },
    {
      raw: "Graph_theory", name: "Graph theory", cluster: 1, score: 0.88,
      rationale: "Hub of Algorithms course. Strong PageRank, weak prerequisites — a soft landing.",
      metrics: { degree: 16, span: 1, size: 9, hasWiki: true, rl: 0.18 },
    },
    {
      raw: "Manifold", name: "Manifold", cluster: 2, score: 0.84,
      rationale: "Mathematical scaffolding for general relativity, control theory, and modern fluid dynamics.",
      metrics: { degree: 12, span: 2, size: 8, hasWiki: true, rl: 0.21 },
    },
    {
      raw: "Shannon_entropy", name: "Shannon entropy", cluster: 5, score: 0.81,
      rationale: "Root of information theory; bridges to biology via mutual information, to ML via cross-entropy.",
      metrics: { degree: 14, span: 1, size: 7, hasWiki: true, rl: 0.15 },
    },
  ];

  // Bridge options when standing at a node — for the lesson view's bridge button.
  function bridgesFrom(nodeId) {
    const node = NODES.find(n => n.id === nodeId);
    if (!node) return [];
    const adj = adjacencyOf(nodeId);
    return adj.filter(n => n.cluster !== node.cluster).map(n => ({
      via: nodeId,
      to: n.id, toName: n.name,
      cluster: n.cluster, clusterName: CLUSTERS[n.cluster].name,
    }));
  }

  // Propose-tab synthesis (canned)
  const PROPOSE_EXAMPLES = {
    "drone swarm coordination": {
      matched: ["State_space", "Graph_theory", "Markov_chain", "Lyapunov_stability", "Synaptic_plasticity"],
      bridges: [
        { from: "State_space", to: "Graph_theory", via: "Each agent is a node; communication topology defines a graph. State of the swarm = product of per-agent states constrained by the graph." },
        { from: "Markov_chain", to: "Synaptic_plasticity", via: "Hebbian-style consensus rules borrow directly from synaptic plasticity. Both are local stochastic update rules that converge to a global pattern." },
      ],
      synthesis: "Swarm coordination reduces, at the algebraic level, to consensus on a graph: the swarm is one extended state-space system whose A-matrix is the negative graph Laplacian. Stability is then a Laplacian eigenvalue question (Lyapunov). The biology bridge is unexpected but real — Hebbian synaptic plasticity is the same local-update-as-global-consensus motif that recent multi-agent work uses for emergent coordination."
    },
    "explain entropy to a physicist": {
      matched: ["Shannon_entropy", "Mutual_information", "Markov_chain", "KL_divergence", "Diffusion"],
      bridges: [
        { from: "Shannon_entropy", to: "Diffusion", via: "Boltzmann's H is Shannon entropy of a microstate distribution; diffusion maximizes it monotonically (the H-theorem)." },
      ],
      synthesis: "For a physicist, the cleanest bridge is: Shannon entropy is the information-theoretic generalization of Boltzmann entropy; the H-theorem becomes a statement about diffusion driving distributions toward maximum entropy. KL divergence then has a thermodynamic reading: it's free-energy distance from equilibrium."
    },
  };

  return {
    CLUSTERS, NODES, EDGES, BRIDGE_PAIRS,
    LESSONS, FOUNDATION_PICKS, PROPOSE_EXAMPLES,
    lessonFor, planTour, adjacencyOf, bridgesFrom,
  };

})();
