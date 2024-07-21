# Cascading Failures in Cyber-Physical System

This repository contains Python code to replicate the findings from the paper ["Cascading Failures on Reliability in Cyber-Physical System"](https://ieeexplore.ieee.org/document/7572896) by Zuyuan Zhang, Wei An, and Fangming Shao. The code models cascading failures in cyber-physical systems and estimates the potential impact of node failures using the k-reliability metric.

## Overview
A cyber-physical system (CPS) consists of two interacting networks: a cyber network overlaying a physical network. Node failures in one network can lead to cascading failures in the other, resulting in system-wide failures. This project implements the k-reliability model to estimate the probability of cascading failures in such systems.

## Usage
1. To run the simulation, execute:
    ```sh
    python main.py
    ```

2. To view the results of the paper, run:
    ```sh
    python results.py
    ```

    Also, you can change the input by using the examples in the `sample.txt` text file.
