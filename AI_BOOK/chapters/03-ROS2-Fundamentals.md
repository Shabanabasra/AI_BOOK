---
id: ros2-fundamentals
title: ROS 2 Fundamentals
sidebar_label: ROS 2 Fundamentals
---

# ROS 2 Fundamentals

ROS 2 (Robot Operating System 2) is an open-source framework for building robot applications. It provides tools, libraries, and conventions that help developers create complex robot behaviors without starting from scratch. ROS 2 improves on the original ROS by supporting real-time systems, multiple platforms, and better security.

## Learning Objectives
By the end of this chapter, you will be able to:
- Understand the purpose and benefits of ROS 2
- Identify key components of a ROS 2 system
- Learn basic ROS 2 concepts like nodes, topics, and messages
- Practice simple hands-on exercises using ROS 2 commands

## Key Concepts
- **Node:** A process that performs computation. Each robot function can run in a separate node.
- **Topic:** A named channel used for sending messages between nodes.
- **Message:** The data structure used to communicate over topics.
- **Publisher:** A node that sends messages on a topic.
- **Subscriber:** A node that receives messages from a topic.
- **Service:** A request/reply mechanism for synchronous communication between nodes.
- **Package:** A collection of nodes, libraries, and configuration files for a robot application.
- **Launch File:** A file that starts multiple nodes and sets up their configuration automatically.

## Hands-on Examples / Exercises
1. **Create a ROS 2 Workspace:**
```bash
mkdir -p ~/ros2_ws/src
cd ~/ros2_ws
colcon build
source install/setup.bash
```

2. **Create a Simple Publisher Node:** Write a basic publisher that sends "Hello World" messages to a topic called "chatter".

3. **Create a Subscriber Node:** Develop a subscriber that listens to the "chatter" topic and prints received messages.

4. **Run Publisher and Subscriber Together:** Launch both nodes simultaneously to see message passing in action.

5. **Use Built-in Tools:** Experiment with `ros2 topic list` and `ros2 topic echo` to inspect active topics in your system.

## Summary / Key Takeaways
- ROS 2 provides a flexible framework for developing robot applications with standardized communication patterns.
- Nodes, topics, and messages form the core communication architecture of ROS 2.
- The pub/sub model enables decoupled, modular robot software design.
- Workspaces and packages help organize code for complex robotic systems.
- ROS 2 supports real-time systems, multiple platforms, and enhanced security compared to ROS 1.