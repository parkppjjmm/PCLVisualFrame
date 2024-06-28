##############################
# 1. Open3D를 사용하여 .ply 파일로부터 포인트 클라우드 데이터를 로드합니다.
# 2. 포인트와 색상 데이터를 NumPy 배열로 변환합니다.
# 3. VTK 포인트 및 색상 배열을 생성하고 데이터를 추가합니다.
# 4. VTK 폴리데이터 객체를 생성하고 포인트 및 색상 데이터를 설정합니다.
# 5. VTK 필터를 설정하여 포인트 데이터를 처리합니다.
# 6. VTK 매퍼와 액터를 생성하고 설정합니다.
# 7. 생성된 VTK 액터를 반환하여 렌더러에 추가하고 화면에 렌더링합니다.


import vtk
from PyQt5 import QtWidgets, QtCore
from vtk.qt.QVTKRenderWindowInteractor import QVTKRenderWindowInteractor
import open3d as o3d
import numpy as np

class VTKVisualizer(QtWidgets.QMainWindow):

    def __init__(self, parent=None): # 메서드는 클래스의 인스턴스가 생성될 때 자동으로 호출되는 생성자
        QtWidgets.QMainWindow.__init__(self, parent)

        self.frame = QtWidgets.QFrame()
        self.vl = QtWidgets.QVBoxLayout()

        # VTK Render Widget
        self.vtkWidget = QVTKRenderWindowInteractor(self.frame)
        self.vl.addWidget(self.vtkWidget)

        # Button for resetting the camera position
        self.reset_button = QtWidgets.QPushButton("Reset")
        self.reset_button.setFixedWidth(self.width() // 10)  # 버튼의 가로 길이를 1/10로 설정
        self.reset_button.clicked.connect(self.reset_camera_position)
        self.vl.addWidget(self.reset_button)

        self.frame.setLayout(self.vl)
        self.setCentralWidget(self.frame)

        self.renderer = vtk.vtkRenderer()
        self.vtkWidget.GetRenderWindow().AddRenderer(self.renderer)
        self.interactor = self.vtkWidget.GetRenderWindow().GetInteractor()

        self.points_actor = self.create_point_cloud_actor()
        self.renderer.AddActor(self.points_actor)

        self.renderer.ResetCamera()

        # Set interactor style
        self.interactor.SetInteractorStyle(vtk.vtkInteractorStyleTrackballCamera())

        self.show()
        self.interactor.Initialize()

        # Save the initial camera parameters
        self.initial_camera_position = self.renderer.GetActiveCamera().GetPosition()
        self.initial_camera_focal_point = self.renderer.GetActiveCamera().GetFocalPoint()
        self.initial_camera_view_up = self.renderer.GetActiveCamera().GetViewUp()

    ### Pointing Cloud Part
    def create_point_cloud_actor(self):
        # .ply 파일 경로
        file_path = r"C:\Users\parkp\Desktop\parkjaemin\PointingCloudLiDAR\roomscan-lidar-ply-sample\source\14 Ladybrook Road 10_ply\14 Ladybrook Road 10.ply"

        pcd = o3d.io.read_point_cloud(file_path) # 포인트 클라우드 데이터 로드
        points = np.asarray(pcd.points) # 포인트 클라우드 데이터 NumPy 배열로 변환(x,y,z) 좌표 포함.
        if pcd.has_colors():
            colors = np.asarray(pcd.colors)
            if colors.max() > 1.0:
                colors /= 255.0
        else:
            colors = np.ones(points.shape) * 0.5  # 색상이 없으면, 기본 색상 (회색)

        ### VTK 포인트 클라우드 생성 
        vtk_points = vtk.vtkPoints() # VTK 포인트 객체를 생성
        vtk_colors = vtk.vtkUnsignedCharArray() # VTK 색상 배열 객체 생성, 색상은 3개이 구성요소 RGB.
        vtk_colors.SetNumberOfComponents(3)

        for point, color in zip(points, colors): # 각 포인터와 색상 데이터를 VTK 포인트 및 색상 배열에 추가
            vtk_points.InsertNextPoint(point) #각 포인트를 VTK 포인트로 추가
            vtk_colors.InsertNextTuple3(*(color * 255)) # 각 색상을 VTK 색상으로 추가, 색상 값은 0-1 범위에서 0-255범위로 변환.

        polydata = vtk.vtkPolyData()
        polydata.SetPoints(vtk_points)
        polydata.GetPointData().SetScalars(vtk_colors)

        vertex_filter = vtk.vtkVertexGlyphFilter()
        vertex_filter.SetInputData(polydata)
        vertex_filter.Update()

        mapper = vtk.vtkPolyDataMapper()
        mapper.SetInputConnection(vertex_filter.GetOutputPort())

        actor = vtk.vtkActor()
        actor.SetMapper(mapper)
        
        return actor # 생성된 VTK 액터 반환

    def reset_camera_position(self):
        camera = self.renderer.GetActiveCamera()
        camera.SetPosition(self.initial_camera_position)
        camera.SetFocalPoint(self.initial_camera_focal_point)
        camera.SetViewUp(self.initial_camera_view_up)
        self.renderer.ResetCamera()
        self.vtkWidget.GetRenderWindow().Render()

if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    window = VTKVisualizer()
    app.exec_()
