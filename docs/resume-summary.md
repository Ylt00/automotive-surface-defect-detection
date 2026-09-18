# 简历版项目说明

## 项目名称

基于 YOLOv8 的汽车零部件表面缺陷检测

## 项目描述

构建六类 NEU-DET 汽车/钢材表面缺陷检测项目，覆盖数据清洗、YOLO 格式校验、YOLOv8n 训练、mAP 评估、推理结果可视化、缺陷尺寸分析和错误案例分析，并使用 GitHub Actions 实现自动化测试。

## 技术栈

Python、PyTorch、Ultralytics YOLO、OpenCV、NumPy、Matplotlib、Git、GitHub Actions

## 简历要点

- 构建 1800 张图片、4189 个缺陷框的六分类表面缺陷检测数据流程。
- 完成 YOLOv8n 基线和 P2 高分辨率检测头对比实验。
- 取得 Precision 0.668、Recall 0.655、mAP50 0.708、mAP50-95 0.361。
- 开发结果拼图、缺陷尺寸分布、训练曲线、混淆矩阵、PR 和 F1 曲线生成流程。
- 记录 P2 在低成本 CPU 对照中未超过基线的负结果，并分析计算量与训练不充分等限制。
- 添加 9 个单元测试和 Python 3.10、3.12 双版本 CI。

## 面试讲解重点

1. 如何将公开工业缺陷数据转换为 YOLO 训练格式。
2. 为什么 224 像素完整基线比 128 像素快速对照更强。
3. 为什么 P2 增加高分辨率层后没有提升 mAP。
4. 如何分析 crazing 和 rolled-in scale 的弱项。
5. 如何通过 GitHub Actions 保证实验代码可复现。