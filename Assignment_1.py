#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Thu Jan 31 16:18:06 2019

Submitted for class MM804 Assignment 1 
       The aim of this assignment is to create multiple view ports to 
       compare different types of representation of objects, namely, 
       wireframe, surface, surface with texture map and texture mapping 
       with Phong shading.
       
Version: Python 2
 
Requirements: VTK Library / apple_obj.obj / apple_texture.jpg

Instructions: 1.install vtk library from vtk.org 
              2.download the texture and object file to the same folder as the code 
              3.run the code 
              
@author: ava sehat niaki
"""

import vtk

#reading the apple object(located inside the code folder) using the vtkOBJReader class 
Apple = vtk.vtkOBJReader()
Apple.SetFileName('apple_obj.obj')
Apple.Update()

#Assigning the mapper for output 1: Mesh Rendering
#The Type of the mapper is set to TopologyPolygon and the 
AppleMapper1 = vtk.vtkPolyDataMapper()
AppleMapper1.SetInputConnection(Apple.GetOutputPort())
AppleMapper1.SetResolveCoincidentTopologyPolygonOffsetParameters(1, 1)
AppleMapper1.SetResolveCoincidentTopologyToPolygonOffset()

#Assigning the mapper for output 2: Texture Rendering 
AppleMapper2 = vtk.vtkPolyDataMapper()
AppleMapper2.SetInputConnection(Apple.GetOutputPort())

#Assigning the mapper for output 3: Solid Rendering 
AppleMapper3 = vtk.vtkPolyDataMapper()
AppleMapper3.SetInputConnection(Apple.GetOutputPort())

#Assigning the mapper for output 4: Illuminated Texture Rendering 
AppleMapper4 = vtk.vtkPolyDataMapper()
AppleMapper4.SetInputConnection(Apple.GetOutputPort())


#reading the apple texture(located inside the code folder) using vtkJPEGReader reader
AppleTexture = vtk.vtkJPEGReader()
AppleTexture.SetFileName('apple_texture.jpg')
AppleTexture.Update()

#Defining the read texture as a variable 
texture = vtk.vtkTexture()

#Debugging the variable output setting based on vtk version
if vtk.VTK_MAJOR_VERSION <= 5:
    texture.SetInput(AppleTexture.GetOutput())
else:
    texture.SetInputConnection(AppleTexture.GetOutputPort())

#Assigning the Actor for output 1: The representation is set to wireframe
AppleActor1 = vtk.vtkActor()
AppleActor1.SetMapper(AppleMapper1)
AppleActor1.GetProperty().SetColor(1, 1, 1)
AppleActor1.GetProperty().SetRepresentationToWireframe()

#Assigning the Actor for output 2: The Texture is set to texture(already assigned)
AppleActor2 = vtk.vtkActor()
AppleActor2.SetMapper(AppleMapper2)
AppleActor2.SetTexture(texture)
AppleActor2.RotateX(90.)

#Assigning the Actor for output 3
AppleActor3 = vtk.vtkActor()
AppleActor3.SetMapper(AppleMapper3)
AppleActor3.RotateX(90.)

#Assigning the Actor for output 4: The Texture is set to texture(already assigned)
AppleActor4 = vtk.vtkActor()
AppleActor4.SetTexture(texture)

#Compute normals of the input object to assign light 
normals = vtk.vtkPolyDataNormals()
normals.SetInputConnection(Apple.GetOutputPort())

#Setting mapper based on aquired normals 
AppleMapper4.SetInputConnection(normals.GetOutputPort())
AppleActor4.SetMapper(AppleMapper4)

#Get object properties and changing the shading, color, ...
prop = AppleActor4.GetProperty()

#Setting shading to Phong
prop.ShadingOn()
prop.SetInterpolationToPhong() 
prop.SetColor(1, 1, 0)
prop.SetDiffuse(0.8) 
prop.SetAmbient(0.25) 
prop.SetSpecular(1.0) 
prop.SetSpecularPower(100.0)

#Set light properties for render
light = vtk.vtkLight ()
light.SetLightTypeToSceneLight()
light.SetAmbientColor(1, 1, 1)
light.SetDiffuseColor(1, 1, 1)
light.SetSpecularColor(1, 1, 1)
light.SetPosition(-100, -100, 50)
light.SetFocalPoint(0,0,0)
light.SetIntensity(0.9)

#creating window 1 containing Representation – Wireframe
ren1 = vtk.vtkRenderer()
ren1.SetViewport(0, 0.5, 0.5, 1)
ren1.AddActor(AppleActor1)
ren1.SetBackground(0.1,0.1,0.1)

#creating window 2 containing Surface with texture map
ren2 = vtk.vtkRenderer()
ren2.SetViewport(0.5, 0.5, 1.0, 1.0)
ren2.AddActor(AppleActor2)
ren2.SetBackground(0.1,0.1,0.1)

#creating window 3 containing Representation – Surface
ren3 = vtk.vtkRenderer()
ren3.SetViewport(0, 0, 0.5, 0.5)
ren3.AddActor(AppleActor3)
ren3.SetBackground(0.1,0.1,0.1)

#creating window 4 containing Representation – Surface with texture map and Phong shading
ren4 = vtk.vtkRenderer()
ren4.SetViewport(0.5, 0, 1.0, 0.5)
ren4.AddActor(AppleActor4)
ren4.AddLight(light)
ren4.SetBackground(0.1,0.1,0.1)

#Initilize the Render window and assign size
renWin = vtk.vtkRenderWindow()
renWin.SetSize(800, 800)

#assign  renderers for multible window output
renWin.AddRenderer(ren1)
renWin.AddRenderer(ren2)
renWin.AddRenderer(ren3)
renWin.AddRenderer(ren4)
renWin.Render()

#create a renderwindowinteractor
iren = vtk.vtkRenderWindowInteractor()
iren.SetRenderWindow(renWin)

#screenshop the created window using the vtkWindowToImageFilter class
windowToImageFilter = vtk.vtkWindowToImageFilter()
windowToImageFilter.SetInput(renWin)
windowToImageFilter.Update()

#Write the captured window to JPEG using the vtkJPEGWriter class
writer = vtk.vtkJPEGWriter()
writer.SetFileName("Rendered_Object.jpeg")
#writer.SetWriteToMemory(1)
writer.SetInputConnection(windowToImageFilter.GetOutputPort())
writer.Write()

# enable user interface interactor
iren.Initialize()
iren.Start()
