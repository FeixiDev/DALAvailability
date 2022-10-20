class DRBD:
    # drbdmon
    def drbdmon(self):
        cmd = f'drbdmon'
        return cmd

    # drbdadm status
    def drbdadm_status(self):
        cmd = f'drbdadm status'
        return cmd

    # drbdsetup status -vs
    def drbdsetup_status(self):
        cmd = f'drbdsetup status -vs'
        return cmd

    # drbdsetup events2
    def check_events(self):
        cmd = f'drbdsetup events2'
        return cmd

    #停止资源的同步
    def stop_sync(self,r_name):
        cmd = f"drbdadm pause-sync {r_name}"
        return cmd

    #停止资源的同步
    def start_sync(self,r_name):
        cmd = f"drbdadm resume-sync {r_name}"
        return cmd

    #提升为primary
    def set_primary(self,r_name):
        cmd = f"drbdadm primary {r_name}"
        return cmd

    #提升为Secondary
    def set_secondary(self,r_name):
        cmd = f"drbdadm secondary {r_name}"
        return cmd


class Linstor:

    def start_controller(self):
        cmd = "systemctl start linstor-controller"
        return cmd

    def start_satellite(self):
        cmd = "systemctl start linstor-satellite"
        return cmd

    # node创建
    def create_node(self, node_name, ip, node_type):
        cmd = f'linstor n create {node_name} {ip} --node-type {node_type}'
        return cmd


    # sotrage pool创建
    def create_sp(self, node_name, sp_type, sp_name, vg_name):
        cmd = f'linstor sp create {sp_type} {node_name} {sp_name} {vg_name}'
        return cmd


    # resource definition创建
    def create_rd(self, rd_name):
        cmd = f'linsotr rd create {rd_name}'
        return cmd


    # volume definition创建
    def create_vd(self, vd_name, vd_size):
        cmd = f'linstor vd create {vd_name} {vd_size}'
        return cmd


    # diskless资源创建
    def create_diskless_resource(self, node_name, resource_name):
        cmd = f'linstor r create {node_name} {resource_name} --diskless'
        return cmd


    # diskful资源创建
    def create_diskful_resource(self, node_name, resource_name, sp_name):
        cmd = f'linstor r create {node_name} {resource_name} --storage-pool {sp_name}'
        return cmd


    # diskful资源自动创建放置到指定数量的存储池中
    def create_diskful_resource_auto(self, resource_name, sp_number):
        cmd = f'linstor r create {resource_name} --auto-place {sp_number}'
        return cmd


    # 资源组创建
    def create_resource_group(self,rg_name,sp_name,place_count):
        cmd = f'linstor rg create {rg_name} --storage-pool {sp_name} --place-count {place_count}'
        return cmd


    # 卷组对应的volume group创建
    def create_volume_group(self,vg_name):
        cmd = f'linstor vg create {vg_name}'
        return cmd


    # 通过卷组创建资源
    def create_resource_by_rg(self,vg_name,resource_name,resource_size):
        cmd = f'linstor rg spawn-resources {vg_name} {resource_name} {resource_size}'
        return cmd


    # 调整资源的的容量大小
    def adjust_resource_size(self, vd_number, resource_name, size):
        cmd = f'linstor vd set-size {resource_name} {vd_number} {size}'
        return cmd


    # 修改DRBD资源的配置()
    def adjust_linstor_resource_settings(self,setting_name,setting_operation,resource_name):
        cmd = f'linstor rd drbd-options --{setting_name} {setting_operation} {resource_name}'
        return cmd


    # 取消修改的DRBD资源的配置()
    def unset_linstor_resource_settings(self,setting_name,setting_operation,resource_name):
        cmd = f'linstor rd drbd-options --unset-{setting_name} {setting_operation} {resource_name}'
        return cmd


    # 查看节点信息
    def check_node(self):
        cmd = f'linstor n l'
        return cmd


    # 查看存储池信息
    def check_sp(self):
        cmd = f'linstor sp l'
        return cmd


    # 查看resource definition信息
    def check_rd(self):
        cmd = f'linstor rd l'
        return cmd


    # 查看volume definition信息
    def check_vd(self):
        cmd = f'linstor vd l'
        return cmd


    # 查看resource group信息
    def check_rg(self):
        cmd = f'linstor rg l'
        return cmd


    # 查看volume group信息
    def check_vg(self,name):
        cmd = f'linstor vg l {name}'
        return cmd


    # 查看resource信息
    def check_resource(self):
        cmd = f'linstor r l'
        return cmd

    def check_resource_detailed(self,r_name):
        cmd = f"linstor r lv | grep {r_name}"
        return cmd


    # 查看error_reports列表信息
    def check_error_reports_list(self):
        cmd = f'linstor error-reports list'
        return cmd


    # 查看error_reports具体某一个report信息
    def check_error_reports_specific(self,report_number):
        cmd = f'linstor error-reports show {report_number}'
        return cmd


    # 删除指定节点
    def delete_node(self,node_name):
        cmd = f'linstor n d {node_name}'
        return cmd


    # 删除指定storage pool
    def delete_sp(self,node_name,sp_name):
        cmd = f'linstor sp d {node_name} {sp_name}'
        return cmd


    # 查看resource详细信息
    def check_resource_lv(self):
        cmd = f'linstor r lv'
        return cmd

    # 删除指定resource definition
    def delete_rd(self,resource_name):
        cmd = f'linstor rd d {resource_name}'
        return cmd


    # 删除指定volume definition
    def delete_vd(self,resource_name,volume_number):
        cmd = f'linstor rd d {resource_name} {volume_number}'
        return cmd


    # 删除指定resource
    def delete_resource(self,node_name,resource_name):
        cmd = f'linstor r d {node_name} {resource_name}'
        return cmd


    # 删除指定resource group
    def delete_resource_group(self,rg_name):
        cmd = f'linstor rg d {rg_name}'
        return cmd


    # 删除指定volume group
    def delete_volume_group(self,vg_name,vg_number):
        cmd = f'linstor vg d {vg_name} {vg_number}'
        return cmd



class LVM:
    # pv创建
    def create_pv(self,path):
        cmd = f'pvcreate {path}'
        return cmd


    # vg创建(传入多个vg名的数组)
    def create_vg(self,pv_name_list,vg_name):
        pv = ''
        for i in pv_name_list:
            pv += i + ''
        cmd = f'vgcreate {vg_name} {pv}'
        return cmd


    # lv创建线形卷
    def create_lv(self,lv_size,lv_name,vg_name):
        cmd = f'lvcreate -L {lv_size} -n {lv_name} {vg_name}'
        return cmd


    # 创建thin pool
    def create_thin_pool(self,thin_pool_size,thin_pool_name,vg_name):
        cmd = f'lvcreate -L {thin_pool_size} --thinpool {thin_pool_name} {vg_name}'
        return cmd


    # 创建thin volume
    def create_thin_volume(self,thin_volume_size,thin_volume_name,thin_pool_name):
        cmd = f'lvcreate -V {thin_volume_size} --thin -n {thin_volume_name} {thin_pool_name}'
        return cmd


    # 创建thin volume的snapshot
    def create_thin_volume_snapshot(self,thin_volume_size,thin_volume_name,thin_pool_name):
        cmd = f'lvcreate -L {thin_volume_size} --snapshot --name {thin_volume_name} {thin_pool_name}'
        return cmd


    # 创建strip volume
    def create_strip_volume(self,strip_volume_size,strip_numbers,strip_size,strip_name,vg_name):
        cmd = f'lvcreate -L {strip_volume_size} -i {strip_numbers} -I {strip_size} -n {strip_name} {vg_name}'
        return cmd


    # 创建mirror volume
    def create_mirror_volume(self,mirror_volume_size,data_volume_name,replica_volume_name,mirror_volume_name,vg_name):
        cmd = f'lvcreate -L {mirror_volume_size} -m1 -n {mirror_volume_name} {vg_name} {data_volume_name} {replica_volume_name}'
        return cmd

    # 对thin pool进行扩容
    def extend_thin_pool(self,extend_sieze,thin_pool_name):
        cmd = f'lvextend -L {extend_sieze} {thin_pool_name}'
        return cmd


    # 对thin volume进行扩容
    def extend_thin_volume(self,extend_sieze,thin_volume_name):
        cmd = f'lvextend -L {extend_sieze} {thin_volume_name}'
        return cmd


    # 对thin volume进行缩减
    def reduce_thin_volume(self,extend_sieze,thin_volume_name):
        cmd = f'lvreduce -L {extend_sieze} {thin_volume_name}'
        return cmd


    # pv整体查看
    def check_pv(self):
        cmd = f'pvs'
        return cmd


    # pv查看详细
    def check_pv_detailed(self,pv_name):
        cmd = f'pvdisplay {pv_name}'
        return cmd


    # pv整盘扫描查看
    def check_pv_scan(self):
        cmd = f'pvscan'
        return cmd

    # vg整体查看
    def check_vg(self):
        cmd = f'vgs'
        return cmd


    # vg查看详细
    def check_vg_detailed(self,vg_name):
        cmd = f'vgdisplay {vg_name}'
        return cmd


    # vg整盘扫描查看
    def check_vg_scan(self):
        cmd = f'vgscan'
        return cmd


    # lv整体查看
    def check_lv(self):
        cmd = f'lvs'
        return cmd


    # lv查看详细
    def check_lv_detailed(self,lv_name):
        cmd = f'lvdisplay {lv_name}'
        return cmd


    # lv整盘扫描查看
    def check_lv_scan(self):
        cmd = f'lvscan'
        return cmd


    # pv删除
    def delete_pv(self,pv_name):
        cmd = f'pvremove {pv_name}'
        return cmd


    # vg删除
    def delete_vg(self,vg_name):
        cmd = f'vgremove {vg_name}'
        return cmd


    # lv删除
    def delete_lv(self,lv_name):
        cmd = f'lvremove {lv_name}'
        return cmd



