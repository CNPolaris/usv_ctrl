
__version__ = '1.2.1'

__author__ = 'Tian xin'

from .grids import (
    area_to_grid,
    area_to_grid_2,
    gen_grids_array,
    grid_to_params,
    grid_to_polygon,
    gps_index_in_grids,
    get_bounds_from_shp,
    get_bounds_from_original_data,
    get_bounds_from_file,
    gps_to_grid,
    gps_to_grids_rect,
    grid_to_polygon_rect,
    print_grid_array,
    remove_obstacle_from_grids,
    insert_obstacle_into_grids,
    check_in_lake,
    convert_params,
    get_grid_by_index,
    get_near_grid_info,
    gen_path_coord_from_grid,
    gen_grid_to_baidu_polygon,
    gps_to_grid
)

from .convert import (
    convert_to_baidu_single,
    convert_by_baidu,
    get_distance_by_baidu,
    convert_to_tencent_single,
    convert_to_tencent,
    gcj02_to_wgs84,
    wgs84_to_gcj02,
    transform_lat,
    transform_lng,
    convert_from_gps_to_shp,
    degree_to_lng_lat,
    transform_degree,
    transform_shape,
    get_flatter_distance,
    get_distance,
    calculate_mileage,
    covert_from_arcgis,
)

from .processing import (
    gps_processing,
    island_processing,
)

from .shp import (
    gps_to_shp
)