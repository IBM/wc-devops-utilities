# Change Track #

This page use to record some function changes or big enhancement ( not include fix commit )

### 2018-7-25 ###
  *  Refine the folder name by change "kubernetes" to "utilities" and old "utilites" to "scritps"
  *  Add new Daily Job -- DBClean
  *  Add new Daily Job -- Clean Cacheivl

### 2018-8-8 ###
   * Add new Job "KubeExec_Base" which support to run shell command in side of target Pods
   * Add EventAgent which will be the exector to work with KubeExec_Base Job to exec defined shell command in side of target Pods
   * Add new Daily Job -- Utilities_StagingProp_Base
   * Add new Daily Job -- Search Index Build and Index Propogation.

### 2018-11-1 ###
   * Generate release version 1.0.0, which fixed some defect caused by python module update.
   * Sync backend scripts for kube log in version 1.0.0.
   * Change the sevice dependece check for ts-app with ping api, the old api has deperated.
   
### 2018-12-13 ###
   * Merge code to support build custom code in Commerce Utilities Docker through Jenkins Job
