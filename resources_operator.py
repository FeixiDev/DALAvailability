class DRBD:
    # drbdmon
    def drbdmon(self):
        cmd = f'drbdmon'

    # drbdadm status
    def drbdadm_status(self):
        cmd = f'drbdadm status'

    # drbdsetup events2
    def check_events(self):
        cmd = f'drbdsetup events2'

    #资源提升为priamry状态
    def drbdadm_priamry(self):
        cmd = f'drbdadm primary fres'
        return cmd

    #恢复为secondary状态
    def drbdadm_secondary(self):
        cmd = f'drbdadm secondary fres'
        return cmd


class Linstor:
    # node创建
    def create_node(self, node_name, ip, node_type):
        cmd = f'linstor n create {node_name} {ip} --node-type {node_type}'

    # sotrage pool创建
    def create_sp(self, node_name, sp_type, sp_name, vg_name):
        cmd = f'linstor sp create {sp_type} {node_name} {sp_name} {vg_name}'

    # resource definition创建
    def create_rd(self, rd_name):
        cmd = f'linsotr rd create {rd_name}'

    # volume definition创建
    def create_vd(self, vd_name, vd_size):
        cmd = f'linstor vd create {vd_name} {vd_size}'

    # diskless资源创建
    def create_diskless_resource(self, node_name, resource_name):
        cmd = f'linstor r create {node_name} {resource_name} --diskless'

    # diskful资源创建
    def create_diskful_resource(self, node_name, resource_name, sp_name):
        cmd = f'linstor r create {node_name} {resource_name} --storage-pool {sp_name}'

    # diskful资源自动创建放置到指定数量的存储池中
    def create_diskful_resource_auto(self, resource_name, sp_number):
        cmd = f'linstor r create {resource_name} --auto-place {sp_number}'

    # 资源组创建
    def create_resource_group(self,rg_name,sp_name,place_count):
        cmd = f'linstor rg create {rg_name} --storage-pool {sp_name} --place-count {place_count}'

    # 卷组对应的volume group创建
    def create_volume_group(self,vg_name):
        cmd = f'linstor vg create {vg_name}'

    # 通过卷组创建资源
    def create_resource_by_rg(self,vg_name,resource_name,resource_size):
        cmd = f'linstor rg spawn-resources {vg_name} {resource_name} {resource_size}'

    # 调整资源的的容量大小
    def adjust_resource_size(self, vd_number, resource_name, size):
        cmd = f'linstor vd set-size {resource_name} {vd_number} {size}'

    # 修改DRBD资源的配置()
    def adjust_linstor_resource_settings(self,setting_name,setting_operation,resource_name):
        cmd = f'linstor rd drbd-options --{setting_name} {setting_operation} {resource_name}'

    # 取消修改的DRBD资源的配置()
    def unset_linstor_resource_settings(self,setting_name,setting_operation,resource_name):
        cmd = f'linstor rd drbd-options --unset-{setting_name} {setting_operation} {resource_name}'

    # 查看节点信息
    def check_node(self):
        cmd = f'linstor n l'

    # 查看存储池信息
    def check_sp(self):
        cmd = f'linstor sp l'

    # 查看resource definition信息
    def check_rd(self):
        cmd = f'linstor rd l'

    # 查看volume definition信息
    def check_vd(self):
        cmd = f'linstor vd l'

    # 查看resource group信息
    def check_rg(self):
        cmd = f'linstor rg l'

    # 查看volume group信息
    def check_vg(self,name):
        cmd = f'linstor vg l {name}'

    # 查看resource信息
    def check_resource(self):
        cmd = f'linstor r l'

    # 查看error_reports列表信息
    def check_error_reports_list(self):
        cmd = f'linstor error-reports list'

    # 查看error_reports具体某一个report信息
    def check_error_reports_specific(self,report_number):
        cmd = f'linstor error-reports show {report_number}'

    # 删除指定节点
    def delete_node(self,node_name):
        cmd = f'linstor n d {node_name}'

    # 删除指定storage pool
    def delete_sp(self,node_name,sp_name):
        cmd = f'linstor sp d {node_name} {sp_name}'

    # 删除指定resource definition
    def delete_rd(self,resource_name):
        cmd = f'linstor rd d {resource_name}'

    # 删除指定volume definition
    def delete_vd(self,resource_name,volume_number):
        cmd = f'linstor rd d {resource_name} {volume_number}'

    # 删除指定resource
    def delete_resource(self,node_name,resource_name):
        cmd = f'linstor r d {node_name} {resource_name}'

    # 删除指定resource group
    def delete_resource_group(self,rg_name):
        cmd = f'linstor rg d {rg_name}'

    # 删除指定volume group
    def delete_volume_group(self,vg_name,vg_number):
        cmd = f'linstor vg d {vg_name} {vg_number}'


class LVM:
    # pv创建
    def create_pv(self,path):
        cmd = f'pvcreate {path}'

    # vg创建(传入多个vg名的数组)
    def create_vg(self,pv_name_list,vg_name):
        pv = ''
        for i in pv_name_list:
            pv += i + ''
        cmd = f'vgcreate {vg_name} {pv}'

    # lv创建线形卷
    def create_lv(self,lv_size,lv_name,vg_name):
        cmd = f'lvcreate -L {lv_size} -n {lv_name} {vg_name}'

    # 创建thin pool
    def create_thin_pool(self,thin_pool_size,thin_pool_name,vg_name):
        cmd = f'lvcreate -L {thin_pool_size} --thinpool {thin_pool_name} {vg_name}'

    # 创建thin volume
    def create_thin_volume(self,thin_volume_size,thin_volume_name,thin_pool_name):
        cmd = f'lvcreate -V {thin_volume_size} --thin -n {thin_volume_name} {thin_pool_name}'

    # 创建thin volume的snapshot
    def create_thin_volume_snapshot(self,thin_volume_size,thin_volume_name,thin_pool_name):
        cmd = f'lvcreate -L {thin_volume_size} --snapshot --name {thin_volume_name} {thin_pool_name}'

    # 创建strip volume
    def create_strip_volume(self,strip_volume_size,strip_numbers,strip_size,strip_name,vg_name):
        cmd = f'lvcreate -L {strip_volume_size} -i {strip_numbers} -I {strip_size} -n {strip_name} {vg_name}'

    # 创建mirror volume
    def create_mirror_volume(self,mirror_volume_size,data_volume_name,replica_volume_name,mirror_volume_name,vg_name):
        cmd = f'lvcreate -L {mirror_volume_size} -m1 -n {mirror_volume_name} {vg_name} {data_volume_name} {replica_volume_name}'

    # 对thin pool进行扩容
    def extend_thin_pool(self,extend_sieze,thin_pool_name):
        cmd = f'lvextend -L {extend_sieze} {thin_pool_name}'

    # 对thin volume进行扩容
    def extend_thin_volume(self,extend_sieze,thin_volume_name):
        cmd = f'lvextend -L {extend_sieze} {thin_volume_name}'

    # 对thin volume进行缩减
    def reduce_thin_volume(self,extend_sieze,thin_volume_name):
        cmd = f'lvreduce -L {extend_sieze} {thin_volume_name}'

    # pv整体查看
    def check_pv(self):
        cmd = f'pvs'

    # pv查看详细
    def check_pv_detailed(self,pv_name):
        cmd = f'pvdisplay {pv_name}'

    # pv整盘扫描查看
    def check_pv_scan(self):
        cmd = f'pvscan'

    # vg整体查看
    def check_vg(self):
        cmd = f'vgs'

    # vg查看详细
    def check_vg_detailed(self,vg_name):
        cmd = f'vgdisplay {vg_name}'

    # vg整盘扫描查看
    def check_vg_scan(self):
        cmd = f'vgscan'

    # lv整体查看
    def check_lv(self):
        cmd = f'lvs'

    # lv查看详细
    def check_lv_detailed(self,lv_name):
        cmd = f'lvdisplay {lv_name}'

    # lv整盘扫描查看
    def check_lv_scan(self):
        cmd = f'lvscan'

    # pv删除
    def delete_pv(self,pv_name):
        cmd = f'pvremove {pv_name}'

    # vg删除
    def delete_vg(self,vg_name):
        cmd = f'vgremove {vg_name}'

    # lv删除
    def delete_lv(self,lv_name):
        cmd = f'lvremove {lv_name}'


