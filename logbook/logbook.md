# Logbook

Meeting (6 May 2025)
Present:  

Yaowen Chang (YC, Student)  

Dr. Yves Plancherel (YP, Main Supervisor)  

Dr. Myriam Prasow-Emond (MP, Co-Supervisor)  

Key points discussed
Project Kick-off & Data Review  

Confirmed the primary project goal: developing an AI pipeline for individual tree canopy segmentation from UAV data to estimate above-ground carbon.  

Reviewed the available dataset: raw multispectral orthomosaics, Digital Surface Model (DSM), and the initial unaligned point cloud.  

Finalized the proposed technical approach: Grounded DINO for object detection, SAM for 2D segmentation, and a projection method to generate 3D labels.

Initial Technical Challenges  

YP highlighted the critical importance of precise co-registration between the 2D orthomosaic and the 3D point cloud as a prerequisite for accurate label projection.  

MP suggested establishing a clear version control workflow and a structured project repository from day one.

Feedback received
Data First: Before any AI work, create robust data loading and preprocessing scripts. Verify the Ground Sample Distance (GSD) and image projections are consistent.

Version Control: Set up the GitHub repository immediately. All code, scripts, and environment files (environment.yml) should be committed.

Baseline Alignment: Perform an initial check on the point cloud vs. orthomosaic alignment to quantify the baseline registration error.

Work plan before next meeting
Setup Repository: Initialize the GitHub project repository with a clear folder structure for data, notebooks, and scripts.

Data Preprocessing: Develop Python scripts to load, preprocess, and visualize the orthomosaic and point cloud data.

Initial Co-registration: Calculate the initial Root Mean Square Error (RMSE) for the geo-alignment between the orthomosaic and the point cloud.

Grounded DINO Demo: Run a basic Grounded DINO demo on a small sample tile using a generic prompt like "tree" to ensure the model environment is working.

Meeting (13 May 2025)
Present:  

Yaowen Chang (YC, Student)  

Dr. Yves Plancherel (YP, Main Supervisor)  

Dr. Myriam Prasow-Emond (MP, Co-Supervisor)  

Key points discussed
Preprocessing & Alignment Status  

YC confirmed that the data loading scripts are functional. The initial alignment check reveals a significant registration error of ~0.5 m RMSE, which is too high for accurate projection.

The basic Grounded DINO demo works correctly and can identify trees in the test tile.

Prompt Engineering & Segmentation Strategy  

Discussed the need to move beyond generic "tree" prompts. The next step is to use more descriptive text prompts (e.g., "pine tree canopy," "oak tree") to improve detection specificity.

The output from Grounded DINO (bounding boxes) will serve as the input for the Segment Anything Model (SAM) to generate precise 2D masks.

Feedback received
Refine Prompts: Experiment with different text prompts to see how Grounded DINO responds to species-specific and context-aware queries.

Address Alignment: The ~0.5 m RMSE is unacceptable. YP recommended implementing an Iterative Closest Point (ICP) algorithm as a first step to improve the coarse alignment of the point cloud.

Focus on 2D First: MP advised perfecting the 2D mask generation (DINO + SAM) before focusing heavily on the 3D projection. A clean 2D result is essential.

Work plan before next meeting
Integrate SAM: Build the first stage of the pipeline combining Grounded DINO's bounding boxes with SAM to generate 2D instance segmentation masks.

Prompt Refinement: Test and document at least five different text prompts and their impact on detection quality.

Implement ICP: Write and apply a script using a library like Open3D or PyVista to perform ICP registration on the point cloud and recalculate the alignment RMSE.

Start AI Log: Begin a log file documenting all model prompts, key parameters, and qualitative results.

Meeting (20 May 2025)
Present:  

Yaowen Chang (YC, Student)  

Dr. Yves Plancherel (YP, Main Supervisor)  

Dr. Myriam Prasow-Emond (MP, Co-Supervisor)  

Key points discussed
2D Segmentation Progress  

YC presented strong initial results from the Grounded DINO → SAM pipeline. The model successfully generates 2D instance masks for individual tree canopies.

Identified issues with noisy detections: small, irrelevant masks are generated for shadows or ground clutter, and some masks are fragmented.

Projection Logic  

The discussion moved to the core logic of projecting the 2D masks onto the 3D point cloud. Key criteria need to be established to decide which points belong to which mask.

ICP algorithm has improved alignment, but a residual error of ~0.3 m RMSE remains, which is still borderline.

Feedback received
Post-processing is Key: MP suggested implementing post-processing filters on the 2D masks. Filter out masks below a certain confidence score (e.g., ≥ 0.35) and a minimum pixel area (e.g., ≥ 200 pixels) to eliminate noise.

Robust Projection Criteria: YP advised against a simple vertical projection. A more robust method should use the Canopy Height Model (CHM) to filter points, ensuring only points within a plausible height range (e.g., CHM ±1 m) are associated with a canopy.

Document Everything: Continue to rigorously document the filtering thresholds and projection logic in the AI log.

Work plan before next meeting
Implement 2D Filters: Add post-processing steps to the 2D pipeline to filter masks based on model confidence and minimum pixel area.

Develop 3D Projection Script: Write the script to project the cleaned 2D masks onto the point cloud, incorporating CHM-based height filtering to create initial 3D pseudo-labels.

Evaluate 2D Segmentation: Create a small, hand-labeled validation set (10-20 canopies) and calculate the mean Intersection over Union (mIoU) for the 2D masks.

Meeting (27 May 2025)
Present:  

Yaowen Chang (YC, Student)  

Dr. Yves Plancherel (YP, Main Supervisor)  

Dr. Myriam Prasow-Emond (MP, Co-Supervisor)  

Key points discussed
First 3D Results & Challenges  

YC demonstrated the first projected 3D pseudo-labels. The CHM filtering has successfully removed most ground points, resulting in much cleaner canopy point clouds.

However, the remaining ~0.3 m alignment error is now clearly visible, causing systematic offsets where labels from one view don't perfectly match points from another.

Refining 3D Labels  

The projected pseudo-labels are a good start but are noisy and lack fine detail at the boundaries. Discussed using a dedicated 3D segmentation model (like Segment3D) to refine these noisy initial labels.

Feedback received
Local Affine Correction: YP insisted the alignment error must be fixed before proceeding. He proposed implementing a local affine correction step after the global ICP to correct for non-rigid distortions, aiming for an RMSE strictly below 0.2 m.

Evaluation Metrics: MP recommended defining the 3D evaluation metrics now. In addition to mIoU, Boundary F-score (BF) should be included to specifically measure edge accuracy, which is critical for carbon models.

Start Visualization: Begin exploring web-based 3D viewers like Potree or Cesium to think about how the final results will be presented.

Work plan before next meeting
Implement Affine Correction: Add a local affine transformation step to the co-registration workflow and tune it to reduce the point cloud vs. orthomosaic RMSE to < 0.2 m.

Integrate Segment3D: Set up the Segment3D model and use the projected point cloud labels as its input to generate cleaner, more accurate 3D instance segments.

Scaffold End-to-End Pipeline: Combine all steps (Grounded DINO → SAM → Projection → Segment3D) into a single, runnable script.

Research Web-GL Dashboard: Investigate technical requirements for building an interactive Web-GL dashboard for results visualization.

Meeting (3 June 2025)
Present:  

Yaowen Chang (YC, Student)  

Dr. Yves Plancherel (YP, Main Supervisor)  

Dr. Myriam Prasow-Emond (MP, Co-Supervisor)  

Key points discussed
Pipeline Nearing Completion

YC reported that the local affine correction was successful, bringing the alignment RMSE down to 0.18 m.

The Segment3D integration is working; it successfully refines the noisy pseudo-labels into coherent 3D segments with instance IDs. The end-to-end pipeline is now functional.

Shift to Evaluation & Uncertainty

With the core pipeline built, the focus now shifts to rigorous evaluation. Discussed creating a validation subset (~500 canopies) with ground-truth labels.

YP introduced the need for uncertainty quantification via a Monte Carlo simulation to understand the error propagation from segmentation to the final carbon estimate.

Feedback received
Major Milestone: Supervisors acknowledged that a functional end-to-end pipeline is a major achievement.

Automate Evaluation: MP stressed the need for automated evaluation scripts. The process of calculating mIoU, BF, and Carbon RMSE should be batched and reproducible, not run manually.

Dashboard Prototype: Now is the time to build a basic prototype of the Web-GL dashboard to visualize a sample segmented point cloud.

Work plan before next meeting
Finalize End-to-End Script: Clean up and comment the full pipeline script to ensure it runs smoothly from start to finish.

Define Evaluation Strategy: Formally define the evaluation metrics (mIoU, BF, Carbon RMSE) and the structure for the validation dataset.

Plan Monte Carlo Simulation: Outline the methodology for the 1,000-run Monte Carlo uncertainty simulation, defining which parameters will be varied.

Build Dashboard Prototype: Create a basic Web-GL viewer that can load and display one of the segmented point cloud outputs.

Meeting (10 June 2025)
Present:  

Yaowen Chang (YC, Student)  

Dr. Yves Plancherel (YP, Main Supervisor)  

Dr. Myriam Prasow-Emond (MP, Co-Supervisor)  

Key points discussed
Full Pipeline Demonstration  

YC demonstrated a successful run of the finalized end-to-end workflow, producing a high-quality segmented point cloud with instance IDs. The alignment RMSE is stable at 0.18 m.

Presented the initial Web-GL dashboard prototype, which successfully loads and displays the 3D model.

Finalizing Evaluation Plan  

The evaluation strategy is set: mIoU and Boundary F-score for segmentation accuracy, and Carbon RMSE for the final application-level error. Target for Carbon RMSE is ≤ 15%.

The plan for the Monte Carlo uncertainty simulation was reviewed and approved.

Feedback received
Dashboard Interactivity: MP suggested adding interactive elements to the dashboard, specifically a panel to display live metrics and controls to switch between different sample areas. This will be vital for stakeholder presentations.

Reproducibility: YP emphasized that all evaluation scripts must be robust and, ideally, integrated into a continuous integration (CI) system like GitHub Actions for automated, reproducible runs.

Methods Documentation: It's time to start formally writing the methods section of the report, including pseudo-code and flowcharts for the key algorithms (e.g., the 3D projection).

Work plan before next meeting
Minimal Case Testing: Select a 100 m × 100 m sub-area and run an end-to-end test to create a clean demo case for the report.

Develop Evaluation Scripts: Write the Python scripts to batch-compute mIoU, BF, and Carbon RMSE over the validation subset and export the results to a CSV file.

Start Monte Carlo Runs: Begin the 1,000-run Monte Carlo simulation.

Draft Methods Section: Start writing the detailed methodology, focusing on the point cloud projection and multi-view fusion strategies.

Iterate on Dashboard: Add the recommended interactive controls (metrics panel, sample switcher) to the Web-GL dashboard.








## Meeting (17 June 2025)

**Present:**  
- Yaowen Chang (YC, Student)  
- Dr. Yves Plancherel (YP, Main Supervisor)  
- Dr. Myriam Prasow-Emond (MP, Co-Supervisor)  

---

### Key points discussed

1. **Pipeline Progress**  
   - YC has completed the multi-stage workflow from raw UAV multispectral orthomosaic to point cloud, implementing the end-to-end Grounded DINO → SAM → 2D pseudo-labels → point cloud projection → Segment3D pipeline, and can output point cloud pseudo-labels with instance IDs (see project plan).  

2. **Evaluation & Uncertainty Quantification**  
   - Discussed evaluating results by mIoU, Boundary F-score, and Carbon RMSE. Supervisors advised focusing on keeping Carbon RMSE ≤ 15% and refining the details of the 1,000-run Monte Carlo uncertainty simulation (see project plan).  

3. **Data Alignment & Error Correction**  
   - YP emphasized that the point cloud vs. orthomosaic alignment residual must be strictly controlled below 0.2 m RMSE, and suggested adding a local affine correction step to reduce registration error (see project plan).  

4. **Interactive Visualization & Deliverables**  
   - MP approved the interactive Web-GL dashboard and recommended adding a live metrics panel (mIoU, BF, RMSE) and a sample-switching control to enhance stakeholder presentations (see project plan).  

---

### Feedback received

- **Minimal Case Testing:**  
  Before running the full scenario, select a 100 m × 100 m sub-area (single tree species) for an end-to-end demo to verify label accuracy in the 2D → 3D projection process.

- **Evaluation Scripts & Reproducibility:**  
  Write scripts to batch-compute mIoU, BF, and RMSE over the validation subset (~500 canopies) and export to CSV. These scripts and data fixtures should be integrated into GitHub Actions for automated runs.

- **Methods Section Detail:**  
  Add pseudo-code and flowcharts for point cloud projection criteria (distance threshold GSD/2, CHM ±1 m) and multi-view fusion voting strategy to ensure reproducibility (see project plan).

- **AI Logging & Traceability:**  
  Document all Grounded DINO/SAM prompts, sample outputs, and post-processing parameters in the appendix, and explain how thresholds were tuned (confidence ≥ 0.35, region ≥ 200 px) (see project plan).

---

### Work plan before next meeting

1. **Minimal Area Validation**  
   - Choose a 100 m × 100 m sub-area with a single tree species, run the full Grounded DINO → SAM → projection → Segment3D pipeline, and produce example point clouds and visual snapshots.

2. **Automated Evaluation Scripts**  
   - Develop and test Python scripts to batch-compute mIoU ≥ 0.75, BF ≥ 0.80, RMSE ≤ 15%, export CSV results, and configure pytest fixtures in GitHub Actions for automated execution.

3. **Uncertainty Simulation Completion**  
   - Perform the 1,000-run Monte Carlo simulation, summarize the 95% confidence interval for total plot carbon C, and include error bar charts in the report.

4. **Methods Section Augmentation**  
   - In the Methods chapter, add:  
     - Point cloud–orthomosaic co-registration workflow (ICP + local affine correction)  
     - Projection algorithm pseudo-code and multi-view fusion strategy  
     - List of generative AI prompts and threshold settings

5. **Dashboard Prototype Iteration**  
   - Enhance the current Web-GL dashboard with a metrics panel and area-switching controls to display evaluation results for different subsets.


## Work (23 June 2025)

**Present:**  
- Yaowen Chang (YC, Student)  
---
1. **Mask the tiff files**  
   - Using GeoSAM to mask the tiff files and do the other job.
work and work

work and work and work

Focus on one step and do one thing

## Work (23 June 2025)

**Present:**  
- Yaowen Chang (YC, Student)  
---
1. **Mask the tiff files**  
   - Using GeoSAM to mask the tiff files and do the other job.
work and work

work and work and work

Focus on one step and do one thing. finished the task.
Logbook
Meeting (24 June 2025)
Present:  

Yaowen Chang (YC, Student)  

Dr. Yves Plancherel (YP, Main Supervisor)  

Dr. Myriam Prasow-Emond (MP, Co-Supervisor)  

Key points discussed
Minimal Area Validation Complete  

YC has successfully completed the end-to-end pipeline test on the 100 m × 100 m sub-area. The results show clear point cloud segmentation snapshots, validating the accuracy of the 2D to 3D label projection, especially in a simple scenario with a single tree species.

Automated Evaluation Scripts Progress  

The Python scripts for batch-computing mIoU, BF, and RMSE have been initially developed. They passed tests on a small-scale dataset and can successfully generate CSV result files.

Dashboard Iteration  

The Web-GL dashboard prototype has been updated to include a live metrics panel and area-switching controls. MP was satisfied with the new features, believing they significantly enhance presentation effectiveness.

Feedback received
Scale Up Evaluation: YP noted that the scripts now need to be stress-tested on the full validation subset (~500 canopies) to ensure their stability and efficiency.

GitHub Actions Integration: MP reminded that the next step is to integrate these evaluation scripts into GitHub Actions for automated testing and reproducibility.

Uncertainty Simulation: The Monte Carlo simulation is one of the most critical remaining tasks and needs to be completed soon, as its results are crucial for the final report.

Work plan before next meeting
Full-Scale Evaluation: Run the automated evaluation scripts on the full validation subset (~500 canopies) and analyze the preliminary results.

GitHub Actions Setup: Configure a GitHub Actions workflow to automatically run the evaluation scripts on code commits.

Complete Monte Carlo Simulation: Complete the 1,000-run Monte Carlo simulation and begin statistical analysis of the results.

Draft Methods Section: Continue drafting the Methods section, specifically the detailed description of the point cloud–orthomosaic co-registration workflow (ICP + local affine correction).

Meeting (1 July 2025)
Present:  

Yaowen Chang (YC, Student)  

Dr. Yves Plancherel (YP, Main Supervisor)  

Dr. Myriam Prasow-Emond (MP, Co-Supervisor)  

Key points discussed
Full Evaluation Results & Analysis  

The evaluation results on the full validation set are in: mIoU ≥ 0.78, BF ≥ 0.82, and Carbon RMSE is approximately 14.2%. All metrics meet the project's target goals.

GitHub Actions has been successfully configured, automatically triggering the evaluation process on each code push.

Monte Carlo Simulation Completed  

The 1,000-run Monte Carlo simulation is complete. Preliminary analysis shows that the 95% confidence interval for total plot carbon has been determined, and the results are as expected.

Methods Section Progress  

The first draft of the Methods section is complete, including the co-registration process, projection algorithm pseudo-code, and generative AI parameter details.

Feedback received
Excellent Progress: Both supervisors highly praised the project's progress, considering the core technical work to be largely complete.

Refine the Narrative: YP suggested that it is now time to start thinking about how to organize these results into a compelling narrative. The report should not only show "what was done" but also explain "why it was done" and "what the results mean."

Visualize Uncertainty: MP recommended creating error bar charts for the Monte Carlo simulation results to visually represent uncertainty in the report and final defense.

Work plan before next meeting
Create Final Figures: Produce the core figures required for the report, including: (1) an end-to-end workflow diagram; (2) error bar charts for the Monte Carlo simulation; and (3) screenshots of the best and worst segmentation cases displayed on the Web-GL dashboard.

Write Results Chapter: Begin writing the 'Results' chapter, systematically presenting the evaluation metrics and uncertainty analysis.

Draft Introduction & Conclusion: Draft the 'Introduction' and 'Conclusion' chapters to build the complete report framework.

Refine Dashboard UI: Perform final cosmetic and minor adjustments to the dashboard's user interface to ensure it is polished for the final presentation.

Meeting (8 July 2025 - 12 August 2025)
During this period, formal weekly meetings were suspended to allow YC to focus on writing the final report. Communication shifted to email and ad-hoc discussions as needed. Key progress milestones are summarized below.

Report Writing: YC completed the full first drafts of the Introduction, Methods, Results, and Conclusion chapters.

Figure Generation: All key figures and visualizations were generated and inserted into the draft report.

Code & Repository Cleanup: The GitHub repository was organized, and a detailed README file was added to ensure code readability and reproducibility.

Appendix Finalization: The appendix was completed, containing all Grounded DINO/SAM prompts, parameter tuning processes, and supplementary figures.

Supervisor Feedback Cycles: YC submitted the draft report to YP and MP and made multiple revisions based on their detailed feedback.

Meeting (19 August 2025)
Present:  

Yaowen Chang (YC, Student)  

Dr. Yves Plancherel (YP, Main Supervisor)  

Dr. Myriam Prasow-Emond (MP, Co-Supervisor)  

Key points discussed
Final Report Review  

Reviewed the near-final draft of the report. The overall structure, content, and presentation of results were approved by the supervisors. Discussed final wording for the Abstract and Acknowledgements.

YP expressed satisfaction with the reproducibility of the methodology, while MP praised the visual impact of the results.

Final Presentation/Defense Preparation  

Discussed the structure for the final defense. The consensus was to frame it as a narrative: start with the core research question, introduce the developed solution, and conclude with a clear summary of the findings and their significance.

MP strongly recommended leveraging the interactive Web-GL dashboard for a live demonstration during the presentation, highlighting it as a key strength.

Feedback received
Final Polish: YP requested a final, thorough proofread of the entire report to catch any remaining grammatical, spelling, or formatting errors.

Practice the Presentation: MP advised YC to conduct at least two or three full practice runs of the presentation to ensure smooth delivery and proper time management.
