# PROJECT: Mechanism-Informed Multi-Fidelity RL for Robust Aerodynamic Design

**0. PROJECT SCOPE AND QUESTIONS**
- [x] Write a 1-page spec with:
    - [x] Object types:
        - Base: 2D airfoil
        - Optional: airfoil + flap or fairing
    - [x] Operating envelope (angles of attack, Re, maybe Mach)
    - [x] Objectives:
        - Robust lift-to-drag across envelope
        - Geometric constraints (min thickness, etc.)
    - [x] Research questions:
        - Robust RL vs narrow RL
        - Multi-fidelity RL vs single-fidelity
        - Mechanism-informed representation vs generic

**1. MECHANISM-INFORMED SHAPE PARAMETERIZATION**
- [x] Implement base airfoil parameterization:
    - [x] Choose scheme (camber + thickness, CST, or Bézier with ~6–10 parameters)
    - [x] Code function: params -> (x, y) airfoil surface coordinates
    - [ ] Enforce:
        - Min thickness everywhere
        - Smooth leading/trailing edges
        - Fixed chord / bounds on camber
- [ ] (Optional) Extend to mechanism variants:
    - [ ] Add flap parameters (hinge location, flap chord, deflection)
    - [ ] OR add small fairing/winglet parameters
- [x] Visualize:
    - [x] Plot a few random samples to confirm shapes look physically plausible

**2. CUSTOM LOW-FIDELITY AERODYNAMIC SIMULATOR**
- [x] Decide on basic physics model:
    - [ ] Option A: Potential-flow / panel method with empirical drag correction
    - [x] Option B: Very coarse CFD (simple 2D grid, few iterations)
- [x] Implement low-fidelity solver:
    - [x] Input: airfoil coordinates + flow condition (AoA, Re, Mach)
    - [ ] Output: CL, CD (and optionally Cm)
- [x] Validate qualitatively:
    - [x] Test on standard NACA shapes
    - [x] Check CL vs AoA trends (roughly linear at small AoA, stall-like drop)
    - [x] Check that CD increases with AoA

**3. HIGH-FIDELITY AERODYNAMIC SIMULATOR (REFINED VERSION)**
- [ ] Build a higher-fidelity variant of the same solver:
    - Finer mesh and/or more iterations
    - More accurate drag estimate (e.g., better boundary-layer treatment)
- [ ] Benchmark:
    - Measure runtime per simulation
    - Compare CL, CD to low-fidelity for several shapes/conditions
    - Quantify bias/variance between fidelities
- [ ] Decide a feasible high-fidelity call budget (e.g., 200–500 total)

**4. ROBUST DESIGN ENVIRONMENT (MDP)**
- [ ] Define state:
    - Current design parameters (airfoil or airfoil+flap)
    - (Optional) Derived features like max thickness, camber, etc.
- [ ] Define action:
    - Small continuous change to each design parameter (bounded step)
- [ ] Define operating-condition sampling:
    - A distribution or discrete set over AoA and Re (and Mach if needed)
- [ ] Define low-fidelity reward:
    - Sample K conditions per step from envelope
    - Run low-fidelity solver to get CL, CD
    - Compute robust metric, e.g.:
        - Mean (L/D) across K conditions
        - Penalties for any condition with L/D below threshold
        - Penalties for geometric violations
- [ ] Define episodes:
    - Fixed number of design steps per episode (e.g., 20–50)
    - Termination criteria if constraints are badly violated
- [ ] Sanity checks:
    - Random-walk runs to see reward distribution
    - Confirm that “obviously bad” shapes yield low eward

**5. NON-RL BASELINE OPTIMIZATION**
- [x] Implement gradient-free optimizer:
    - Use CMA-ES or similar on the same parameter vector and reward
- [x] Run baseline optimization with low-fidelity solver:
    - Track robust reward vs number of evaluations
    - Save best designs
- [x] Evaluate best baseline designs across dense condition grid (low-fidelity):
    - Plot L/D vs AoA and Re
    - Compute mean and worst-case L/D over envelope

**6. SINGLE-FIDELITY RL (LOW-FIDELITY ONLY)**
- [ ] Choose RL algorithm (e.g., PPO or SAC) for continuous actions
- [ ] Implement environment wrapper for RL:
    - Reset -> initial design
    - Step(action) -> new design, reward, done, info
- [ ] Train “narrow” RL agent:
    - Single nominal condition (one AoA, one Re)
    - Log training curve (reward vs steps)
- [ ] Train “robust” RL agent:
    - Samples conditions from full envelope each episode
    - Log training curve
- [ ] Evaluate final policies/designs (low-fidelity):
    - Dense grid over conditions
    - Plot:
        - L/D vs AoA (for several Re)
        - Mean and worst-case L/D over envelope
    - Compare narrow vs robust RL vs baseline optimizer

**7. MULTI-FIDELITY RL STRATEGIES**
- [ ] Strategy A: Low-fidelity pre-training + high-fidelity fine-tuning
    - Use robust low-fidelity RL model as initialization
    - Switch reward to high-fidelity solver
    - Fine-tune with limited high-fidelity call budget
- [ ] Strategy B: Mixed-fidelity training
    - During training:
        - Use low-fidelity solver for most steps
        - Occasionally select promising designs for high-fidelity evaluation
        - Adjust rewards/advantages using high-fidelity samples
- [ ] High-fidelity-only baseline:
    - Train RL from scratch using only high-fidelity within same budget
- [ ] Evaluation (all using high-fidelity):
    - For each strategy:
        - Plot robust high-fidelity reward vs number of high-fidelity calls
        - Evaluate final best designs over dense condition grid
    - Compare sample efficiency and final performance

**8. REPRESENTATION STUDY: MECHANISM-INFORMED VS GENERIC**
- [ ] Implement generic shape representation:
    - Example: spline control points or direct coordinate offsets
    - Maintain similar parameter dimensionality as mechanism-informed version
- [ ] Train RL (with chosen multi-fidelity scheme) using generic representation:
    - Same envelope, rewards, algorithms
- [ ] Compare to mechanism-informed representation:
    - Learning speed and stability (reward vs steps)
    - Final robust performance (mean/worst-case L/D)
    - Sensitivity to hyperparameters and random seeds
- [ ] Visualize:
    - Example designs from each representation
    - Pressure distribution and flow snapshots for selected designs

**9. (OPTIONAL) MULTI-SCENARIO / MECHANISM GENERALIZATION**
- [ ] Define scenarios:
    - Scenario A: airfoil only
    - Scenario B: airfoil + flap (or fairing)
- [ ] Extend environment to handle scenario flag:
    - Input includes scenario type
    - Parameter vector includes shared + scenario-specific parameters
- [ ] Train:
    - Single policy conditioned on scenario flag (multi-task RL)
    - Or train on A, fine-tune on B (transfer)
- [ ] Evaluate:
    - Performance in each scenario separately
    - Transfer efficiency (A -> B) vs training B from scratch

**10. ANALYSIS, FIGURES, AND WRITE-UP**
- [ ] Choose 3–4 core comparisons:
    - Robust vs narrow RL
    - Multi-fidelity vs single-fidelity RL
    - Mechanism-informed vs generic representation
    - (Optional) Multi-scenario generalization
- [ ] Generate figures:
    - Learning curves for key agents
    - Robust performance (mean/worst-case L/D) across envelope
    - High-fidelity performance vs high-fidelity call count
    - Example shapes and flow fields (baseline vs optimized)
- [ ] Draft write-up:
    - [ ] Abstract (LACSEF/ISEF style)
    - [ ] Methods (MDP, simulators, RL algorithms, parameterizations)
    - [ ] Results (with the chosen key comparisons)
    - [ ] Discussion (implications of mechanism-informed, multi-fidelity RL)
- [ ] Build science fair materials:
   - [ ] Poster/board layout with diagrams and plots
   - [ ] Short, clear explanation of what “mechanism-informed” and “multi-fidelity” mean