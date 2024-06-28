##############################
# 1. Open3D를 사용하여 .ply 파일로부터 포인트 클라우드 데이터를 로드합니다.
# 2. 포인트와 색상 데이터를 NumPy 배열로 변환합니다.
# 3. VTK 포인트 및 색상 배열을 생성하고 데이터를 추가합니다.
# 4. VTK 폴리데이터 객체를 생성하고 포인트 및 색상 데이터를 설정합니다.
# 5. VTK 필터를 설정하여 포인트 데이터를 처리합니다.
# 6. VTK 매퍼와 액터를 생성하고 설정합니다.
# 7. 생성된 VTK 액터를 반환하여 렌더러에 추가하고 화면에 렌더링합니다.



### VTKVisualizer 클래스 초기화 및 GUI 설정
class VTKVisualizer(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        QtWidgets.QMainWindow.__init__(self, parent)

        self.frame = QtWidgets.QFrame()
        self.vl = QtWidgets.QVBoxLayout()
### 
VTKVisualizer 클래스는 QtWidgets.QMainWindow를 상속받아 GUI 애플리케이션의 메인 윈도우를 만듭니다.
__init__ 메서드는 클래스의 생성자입니다. 부모 클래스 QMainWindow를 초기화합니다.
self.frame는 메인 프레임을 생성합니다.
self.vl는 프레임 안에 위젯을 수직으로 배치하기 위한 레이아웃입니다.


### VTK Render Widget 및 버튼 설정
        self.vtkWidget = QVTKRenderWindowInteractor(self.frame)
        self.vl.addWidget(self.vtkWidget)

        self.reset_button = QtWidgets.QPushButton("Reset")
        self.reset_button.setFixedWidth(self.width() // 10)
        self.reset_button.clicked.connect(self.reset_camera_position)
        self.vl.addWidget(self.reset_button)

        self.frame.setLayout(self.vl)
        self.setCentralWidget(self.frame)
###
self.vtkWidget는 VTK와 PyQt5를 연결하는 위젯입니다.
self.vl.addWidget(self.vtkWidget)로 VTK 위젯을 레이아웃에 추가합니다.
self.reset_button는 카메라 위치를 리셋하는 버튼입니다.
self.reset_button.clicked.connect(self.reset_camera_position)로 버튼 클릭 시 reset_camera_position 메서드가 호출되도록 연결합니다.
self.frame.setLayout(self.vl)로 레이아웃을 프레임에 설정합니다.
self.setCentralWidget(self.frame)로 프레임을 메인 윈도우의 중앙 위젯으로 설정합니다.

### VTK 렌더러 및 인터랙터 설정
        self.renderer = vtk.vtkRenderer()
        self.vtkWidget.GetRenderWindow().AddRenderer(self.renderer)
        self.interactor = self.vtkWidget.GetRenderWindow().GetInteractor()

        self.points_actor = self.create_point_cloud_actor()
        self.renderer.AddActor(self.points_actor)

        self.renderer.ResetCamera()

        self.interactor.SetInteractorStyle(vtk.vtkInteractorStyleTrackballCamera())

        self.show()
        self.interactor.Initialize()

###
self.renderer는 VTK 렌더러 객체를 생성합니다.
self.vtkWidget.GetRenderWindow().AddRenderer(self.renderer)로 VTK 렌더러를 렌더링 윈도우에 추가합니다.
self.interactor는 VTK 인터랙터 객체를 가져옵니다.
self.points_actor는 포인트 클라우드 액터를 생성하는 메서드입니다.
self.renderer.AddActor(self.points_actor)로 렌더러에 포인트 클라우드 액터를 추가합니다.
self.renderer.ResetCamera()로 카메라를 초기화합니다.
self.interactor.SetInteractorStyle(vtk.vtkInteractorStyleTrackballCamera())로 카메라 인터랙션 스타일을 설정합니다.
self.show()로 메인 윈도우를 표시합니다.
self.interactor.Initialize()로 인터랙터를 초기화합니다.

### 초기 카메라 위치 저장
        self.initial_camera_position = self.renderer.GetActiveCamera().GetPosition()
        self.initial_camera_focal_point = self.renderer.GetActiveCamera().GetFocalPoint()
        self.initial_camera_view_up = self.renderer.GetActiveCamera().GetViewUp()

###
초기 카메라의 위치, 초점, 뷰 업 벡터를 저장하여 나중에 카메라 위치를 리셋할 때 사용합니다.


### 포인트 클라우드 액터 생성 메서드

    def create_point_cloud_actor(self):
        file_path = r"D:\DataSample\dronsample.ply"

        pcd = o3d.io.read_point_cloud(file_path)
        points = np.asarray(pcd.points)
        if pcd.has_colors():
            colors = np.asarray(pcd.colors)
            if colors.max() > 1.0:
                colors /= 255.0
        else:
            colors = np.ones(points.shape) * 0.5

        vtk_points = vtk.vtkPoints()
        vtk_colors = vtk.vtkUnsignedCharArray()
        vtk_colors.SetNumberOfComponents(3)

        for point, color in zip(points, colors):
            vtk_points.InsertNextPoint(point)
            vtk_colors.InsertNextTuple3(*(color * 255))

        polydata = vtk.vtkPolyData()
        polydata.SetPoints(vtk_points)
        polydata.GetPointData().Set과

![pointcloudexample](https://github.com/parkppjjmm/PointingCloudLiDAR/assets/56201670/85f1f241-3d21-4d4a-8715-3c00d3c65d30)
