![RTS Logo](https://i.ibb.co/nR1318Q/RTSLogo-Web.png "Realistic Traffic Simulation (RTS) Logo")

Realistic Traffic Simulations (RTS) Repository _(Graduation Project of Egemen Güngör & Sefa Şenlik)_

### v0.3 Features
- **Lane-changing**
- Curved road with _parallel lanes_
- 4 different vehicle models
- 3 different driver types
- Vehicle labeling
- Chase camera
- Traffic lights
- Road imperfections
- Day/night options
- Multiple Lanes
- A couple of dozens of cars

# Realistic Traffic Simulations (RTS)

RTS is an innovative traffic simulation environment that focuses on different aspects and root causes of traffic congestion problems. Rather than conventional solutions, RTS analyzes the impact of driver behavior, road conditions, and vehicle dynamics.

## Key Features

- **Realistic Driver Behavior Simulation**
  - Multiple driver profiles (rookie, hasty, professional)
  - Dynamic vision range based on driver age
  - Progressive acceleration/deceleration patterns
  - Lane changing decisions based on traffic conditions

- **Various Vehicle Types**
  - Multiple vehicle classes (sedan, bus, van, truck)
  - Different sizes and agility characteristics
  - Dynamic following distance capabilities
  - Realistic movement patterns on curved roads

- **Advanced Road System**
  - Support for multi-lane roads with dynamic width
  - Polynomial-based curved road generation
  - Road imperfections and defects
  - Traffic light integration

- **Environmental Factors**
  - Day/night cycle effects on driver behavior
  - Dynamic lighting conditions
  - Road surface variations
  - Weather impact on driving conditions

## Technical Architecture

The project consists of three main components:

1. **Simulation Backend**
   - Core simulation engine (Python-based)
   - Vehicle and driver behavior algorithms
   - Traffic flow calculations
   - Data logging system

2. **3D Visualization (Blender)**
   - Real-time 3D rendering
   - Dynamic camera movements
   - Vehicle model integration
   - Environmental effects

3. **Graphical User Interface**
   - Simulation parameter controls
   - Real-time monitoring
   - Results visualization
   - Configuration management

## Technologies Used

- **Core Development**
  - Python
  - NumPy
  - Matplotlib
  - OpenPyXL

- **3D Visualization**
  - Blender
  - BPY Library
  - EEVEE Render Engine

- **User Interface**
  - Tkinter
  - PIL (Python Imaging Library)

## Future Development

- Junction and intersection modeling
- Pedestrian crossing simulation
- Enhanced physics engine integration
- Bidirectional road support
- Weather condition effects
- Expanded vehicle dynamics
- Simulation state saving/loading

## Acknowledgements

- Assistant Professor Furkan Kıraç for project supervision
- Python and Blender communities for technical support
- HDRIHaven.com for environment textures

## Authors

- Egemen Güngör
- Sefa Şenlik

## Screenshots
![RTS - Accident](https://i.ibb.co/YFW4QnFh/Accident.png "Sedan driver goes past an accident")
![RTS - Day/Night Difference]([https://i.ibb.co/vvvhSZkV/Day-Night-Difference.png "Day/night lighting difference")
![RTS - Traffic Light](https://i.ibb.co/2rbMYzX/RedLight.png "Traffic light goes from from green to red, van driver stops")
