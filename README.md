# 📊 TDD Analysis in Open Source Python Projects

This repository contains a Python-based tool that analyzes the relationship between **Test-Driven Development (TDD) adoption** and software quality/velocity metrics in open-source Python projects.

Specifically, it compares:
- ✅ **TDD Rate vs Bug Rate** (Are projects that follow TDD practices less prone to bugs?)
- ✅ **TDD Rate vs Commit Rate** (Does TDD affect development speed?)

## 🔍 Overview

Test-Driven Development (TDD) is a software development practice where tests are written before writing the corresponding production code. While many believe TDD leads to higher quality software, the actual impact on bug rates and developer productivity is still debated.

This tool aims to analyze this impact across multiple real-world open-source Python projects hosted on GitHub.

---

## 📁 Project Structure

📂 TDDBugandCommitRate/
│── 📄 bugandcommitrate_python.py : contains the program to generate the images of the comparison.
│── 📄 apache_python_projects.json : contains the list of python projects in json (git repo url).
│── 📄 tdd_metric_python: contains the previously calculated tdd rate for all python projects in json.
│── 📄 README.md   # This file (provides description about the coursework)
│── 📂 reference_diagrams_new_rate: contains the results.