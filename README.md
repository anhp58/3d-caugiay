# 3d-caugiay
# source - Source code
  * const.py: Constant variables
  * data_stat.py: Thống kê dữ liệu chiều cao
  * download_gge_img.py: Tự động download ảnh theo tọa độ 
  * extent_opening.py: Tạo ảnh mở rộng / thu nhỏ theo tọa độ và offset
  * extraction_and_training.py: Trích xuất đặc trưng và huấn luyện mô hình
  * height_prediction.py: Tính toán chiều cao
  * masking.py: Tạo ảnh mask cắt về các tòa nhà
  * sampling.py: Lấy mẫu dữ liệu huấn luyện mô hình dựa vào các chỉ số thống kê dữ liệu chiều cao
# fmw - FMW workspaces
  * 5675-citygml-sample-lod2-from-shapefile.fmw / esrishape_esrishape_esrishape2skp_skp.fmw - Workspace generate 3D LoD2 model
  * aq_height_to_3d.fmw - Workspace generate 3D model ONKK
# data 
  * train - Dữ liệu huấn luyện
  * test - Dữ liệu huấn luyện
  * csv_polygon.csv - Dữ liệu lat lon để đưa vào application download ảnh Google Earth
