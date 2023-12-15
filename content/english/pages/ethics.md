---
title: "Ethics & Responsible Use Statement"
# meta title
meta_title: "Ethics Statement"
# meta description
description: "A statement of the ethics and responsible use facets of this project."
# save as draft
draft: false
---

<!-- Please prepare a Statement of Potential Negative Societal Impacts based on the framing from CVPR. We expect that Section 3 won’t apply to everyone, but if it does, please address that as well. (https://cvpr2022.thecvf.com/ethics-guidelines)

Please prepare a statement of principles of responsible use of the technique or system you create. What sorts of contexts or applications would license your work to be used within? What guidelines or restrictions would you place on its use in these situations? -->

## Introduction
This project acknowledges and adheres to ethical standards to ensure responsible use of information. This project is focused on navigating outdoor pathways through computer vision procedures. This is a significantly difficult challenge as there are many inconsistencies even on paved roads like sidewalks. Some of the visual obstacles include shadows, foliage debris, concrete patterns, tar lines, manholes, and general changes in lighting. 
The approach to this issue hinged on a singular assumption. To dynamically update the road state, a region of interest directly in front of the vehicle defines the changing road appearance. In this way, the algorithm can update its path accommodating for the visual obstacles in the road. However since the algorithm is not categorizing these visual obstacles as acceptable road features or not, this algorithm is not optimized for the safety of passersby. 

## Potential Negative Societal Impacts

The algorithm as currently developed is unable to categorize visual obstacles which may lead to safety hazards for pedestrians, cyclists, or other road users, potentially resulting in injuries. In order for this type of outdoor navigation to be implemented with best ethical practice, a high priority must be given to the development and accuracy of detecting objects in real time. 
While the current application is not using any machine learning model to aid its navigation, implementing one to identify obstacles would be a logical next step. As with any machine learning model, especially when categorizing data to recognize humans, there are major privacy and diversity concerns. The collection of data must be acquired ethically via informed and consenting parties. This is of course offset by the priority of accuracy which requires a large plethora of data to train models. 
The other potential ethical risk comes with the scope of outdoor navigation itself. The types of applications for outdoor navigation may range from agriculture to military defense purposes. This camera navigation is not inherently dangerous. However, its widespread use as a foundation for robot perception could lead to projects that overlook the consideration of ethical consequences.

## Final Remarks

This project understands and commits itself to upholding ethical standards in navigating outdoor pathways using computer vision. The algorithm’s challenge lies in its inability to effectively categorize visual obstacles, posing safety risks for pedestrians. Future development should prioritize accuracy. This may be done through the use of a machine learning algorithm, however this approach must pay careful attention to proper procedures to acquire data ethically. The broad application of outdoor navigation emphasizes the diligence all projects must display in considering ethical consequences. 

