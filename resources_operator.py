import utils


class DRBD(object):

    # drbdmon
    def drbdmon(self, ssh_conn=None):
        cmd = f'drbdmon'
        result = utils.exec_cmd(cmd, ssh_conn)
        return result

    # drbdadm status
    def drbdadm_status(self, ssh_conn=None):
        cmd = f'drbdadm status'
        result = utils.exec_cmd(cmd, ssh_conn)
        return result

    # drbdsetup status -vs
    def drbdsetup_status(self, ssh_conn=None):
        cmd = f'drbdsetup status -vs'
        result = utils.exec_cmd(cmd, ssh_conn)
        return result

    # drbdsetup events2
    def check_events(self, ssh_conn=None):
        cmd = f'drbdsetup events2'
        result = utils.exec_cmd(cmd, ssh_conn)
        return result

    # 停止资源的同步
    def stop_sync(self, r_name, ssh_conn=None):
        cmd = f"drbdadm pause-sync {r_name}"
        result = utils.exec_cmd(cmd, ssh_conn)
        return result

    # 停止资源的同步
    def start_sync(self, r_name, ssh_conn=None):
        cmd = f"drbdadm resume-sync {r_name}"
        result = utils.exec_cmd(cmd, ssh_conn)
        return result

    # 提升为primary
    def set_primary(self, r_name, ssh_conn=None):
        cmd = f"drbdadm primary {r_name}"
        result = utils.exec_cmd(cmd, ssh_conn)
        return result

    # 提升为Secondary
    def set_secondary(self, r_name, ssh_conn=None):
        cmd = f"drbdadm secondary {r_name}"
        result = utils.exec_cmd(cmd, ssh_conn)
        return result

    # 资源提升为priamry状态
    def drbdadm_priamry(self, ssh_conn=None):
        cmd = f'drbdadm primary fres'
        result = utils.exec_cmd(cmd, ssh_conn)
        return result

    # 恢复为secondary状态
    def drbdadm_secondary(self, ssh_conn=None):
        cmd = f'drbdadm secondary fres'
        result = utils.exec_cmd(cmd, ssh_conn)
        return result


class Linstor(object):
    def start_controller(self, ssh_conn=None):
        cmd = "systemctl start linstor-controller"
        result = utils.exec_cmd(cmd, ssh_conn)
        return result

    def start_satellite(self, ssh_conn=None):
        cmd = "systemctl start linstor-satellite"
        result = utils.exec_cmd(cmd, ssh_conn)
        return result

    # node创建
    def create_node(self, node_name, ip, node_type, ssh_conn=None):
        cmd = f'linstor n create {node_name} {ip} --node-type {node_type}'
        result = utils.exec_cmd(cmd, ssh_conn)
        return result

    # sotrage pool创建
    def create_sp(self, node_name, sp_type, sp_name, vg_name, ssh_conn=None):
        cmd = f'linstor sp create {sp_type} {node_name} {sp_name} {vg_name}'
        result = utils.exec_cmd(cmd, ssh_conn)
        return result

    # resource definition创建
    def create_rd(self, rd_name, ssh_conn=None):
        cmd = f'linsotr rd create {rd_name}'
        result = utils.exec_cmd(cmd, ssh_conn)
        return result

    # volume definition创建
    def create_vd(self, vd_name, vd_size, ssh_conn=None):
        cmd = f'linstor vd create {vd_name} {vd_size}'
        result = utils.exec_cmd(cmd, ssh_conn)
        return result

    # diskless资源创建
    def create_diskless_resource(self, node_name, resource_name, ssh_conn=None):
        cmd = f'linstor r create {node_name} {resource_name} --diskless'
        result = utils.exec_cmd(cmd, ssh_conn)
        return result

    # diskful资源创建
    def create_diskful_resource(self, node_name, resource_name, sp_name, ssh_conn=None):
        cmd = f'linstor r create {node_name} {resource_name} --storage-pool {sp_name}'
        result = utils.exec_cmd(cmd, ssh_conn)
        return result

    # diskful资源自动创建放置到指定数量的存储池中
    def create_diskful_resource_auto(self, resource_name, sp_number, ssh_conn=None):
        cmd = f'linstor r create {resource_name} --auto-place {sp_number}'
        result = utils.exec_cmd(cmd, ssh_conn)
        return result

    # 资源组创建
    def create_resource_group(self, rg_name, sp_name, place_count, ssh_conn=None):
        cmd = f'linstor rg create {rg_name} --storage-pool {sp_name} --place-count {place_count}'
        result = utils.exec_cmd(cmd, ssh_conn)
        return result

    # 卷组对应的volume group创建
    def create_volume_group(self, vg_name, ssh_conn=None):
        cmd = f'linstor vg create {vg_name}'
        result = utils.exec_cmd(cmd, ssh_conn)
        return result

    # 通过卷组创建资源
    def create_resource_by_rg(self, vg_name, resource_name, resource_size, ssh_conn=None):
        cmd = f'linstor rg spawn-resources {vg_name} {resource_name} {resource_size}'
        result = utils.exec_cmd(cmd, ssh_conn)
        return result

    # 调整资源的的容量大小
    def adjust_resource_size(self, vd_number, resource_name, size, ssh_conn=None):
        cmd = f'linstor vd set-size {resource_name} {vd_number} {size}'
        result = utils.exec_cmd(cmd, ssh_conn)
        return result

    # 修改DRBD资源的配置()
    def adjust_linstor_resource_settings(self, setting_name, setting_operation, resource_name, ssh_conn=None):
        cmd = f'linstor rd drbd-options --{setting_name} {setting_operation} {resource_name}'
        result = utils.exec_cmd(cmd, ssh_conn)
        return result

    # 取消修改的DRBD资源的配置()
    def unset_linstor_resource_settings(self, setting_name, setting_operation, resource_name, ssh_conn=None):
        cmd = f'linstor rd drbd-options --unset-{setting_name} {setting_operation} {resource_name}'
        result = utils.exec_cmd(cmd, ssh_conn)
        return result

    # 查看节点信息
    def check_node(self, ssh_conn=None):
        cmd = f'linstor n l'
        result = utils.exec_cmd(cmd, ssh_conn)
        return result

    # 查看存储池信息
    def check_sp(self, ssh_conn=None):
        cmd = f'linstor sp l'
        result = utils.exec_cmd(cmd, ssh_conn)
        return result

    # 查看resource definition信息
    def check_rd(self, ssh_conn=None):
        cmd = f'linstor rd l'
        result = utils.exec_cmd(cmd, ssh_conn)
        return result

    # 查看volume definition信息
    def check_vd(self, ssh_conn=None):
        cmd = f'linstor vd l'
        result = utils.exec_cmd(cmd, ssh_conn)
        return result

    # 查看resource group信息
    def check_rg(self, ssh_conn=None):
        cmd = f'linstor rg l'
        result = utils.exec_cmd(cmd, ssh_conn)
        return result

    # 查看volume group信息
    def check_vg(self, name, ssh_conn=None):
        cmd = f'linstor vg l {name}'
        result = utils.exec_cmd(cmd, ssh_conn)
        return result

    # 查看resource信息
    def check_resource(self, ssh_conn=None):
        cmd = f'linstor r l'
        result = utils.exec_cmd(cmd, ssh_conn)
        return result

    def check_resource_detailed(self, r_name, ssh_conn=None):
        cmd = f"linstor r lv | grep {r_name}"
        result = utils.exec_cmd(cmd, ssh_conn)
        return result

    # 查看error_reports列表信息
    def check_error_reports_list(self, ssh_conn=None):
        cmd = f'linstor error-reports list'
        result = utils.exec_cmd(cmd, ssh_conn)
        return result

    # 查看error_reports具体某一个report信息
    def check_error_reports_specific(self, report_number, ssh_conn=None):
        cmd = f'linstor error-reports show {report_number}'
        result = utils.exec_cmd(cmd, ssh_conn)
        return result

    # 删除指定节点
    def delete_node(self, node_name, ssh_conn=None):
        cmd = f'linstor n d {node_name}'
        result = utils.exec_cmd(cmd, ssh_conn)
        return result

    # 删除指定storage pool
    def delete_sp(self, node_name, sp_name, ssh_conn=None):
        cmd = f'linstor sp d {node_name} {sp_name}'
        result = utils.exec_cmd(cmd, ssh_conn)
        return result

    # 查看resource详细信息
    def check_resource_lv(self, ssh_conn=None):
        cmd = f'linstor r lv'
        result = utils.exec_cmd(cmd, ssh_conn)
        return result

    # 删除指定resource definition
    def delete_rd(self, resource_name, ssh_conn=None):
        cmd = f'linstor rd d {resource_name}'
        result = utils.exec_cmd(cmd, ssh_conn)
        return result

    # 删除指定volume definition
    def delete_vd(self, resource_name, volume_number, ssh_conn=None):
        cmd = f'linstor rd d {resource_name} {volume_number}'
        result = utils.exec_cmd(cmd, ssh_conn)
        return result

    # 删除指定resource
    def delete_resource(self, node_name, resource_name, ssh_conn=None):
        cmd = f'linstor r d {node_name} {resource_name}'
        result = utils.exec_cmd(cmd, ssh_conn)
        return result

    # 删除指定resource group
    def delete_resource_group(self, rg_name, ssh_conn=None):
        cmd = f'linstor rg d {rg_name}'
        result = utils.exec_cmd(cmd, ssh_conn)
        return result

    # 删除指定volume group
    def delete_volume_group(self, vg_name, vg_number, ssh_conn=None):
        cmd = f'linstor vg d {vg_name} {vg_number}'
        result = utils.exec_cmd(cmd, ssh_conn)
        return result


class LVM(object):
    # pv创建
    def create_pv(self, path, ssh_conn=None):
        cmd = f'pvcreate {path}'
        result = utils.exec_cmd(cmd, ssh_conn)
        return result

    # vg创建(传入多个vg名的数组)
    def create_vg(self, pv_name_list, vg_name, ssh_conn=None):
        pv = ''
        for i in pv_name_list:
            pv += i + ''
        cmd = f'vgcreate {vg_name} {pv}'
        result = utils.exec_cmd(cmd, ssh_conn)
        return result

    # lv创建线形卷
    def create_lv(self, lv_size, lv_name, vg_name, ssh_conn=None):
        cmd = f'lvcreate -L {lv_size} -n {lv_name} {vg_name}'
        result = utils.exec_cmd(cmd, ssh_conn)
        return result

    # 创建thin pool
    def create_thin_pool(self, thin_pool_size, thin_pool_name, vg_name, ssh_conn=None):
        cmd = f'lvcreate -L {thin_pool_size} --thinpool {thin_pool_name} {vg_name}'
        result = utils.exec_cmd(cmd, ssh_conn)
        return result

    # 创建thin volume
    def create_thin_volume(self, thin_volume_size, thin_volume_name, thin_pool_name, ssh_conn=None):
        cmd = f'lvcreate -V {thin_volume_size} --thin -n {thin_volume_name} {thin_pool_name}'
        result = utils.exec_cmd(cmd, ssh_conn)
        return result

    # 创建thin volume的snapshot
    def create_thin_volume_snapshot(self, thin_volume_size, thin_volume_name, thin_pool_name, ssh_conn=None):
        cmd = f'lvcreate -L {thin_volume_size} --snapshot --name {thin_volume_name} {thin_pool_name}'
        result = utils.exec_cmd(cmd, ssh_conn)
        return result

    # 创建strip volume
    def create_strip_volume(self, strip_volume_size, strip_numbers, strip_size, strip_name, vg_name, ssh_conn=None):
        cmd = f'lvcreate -L {strip_volume_size} -i {strip_numbers} -I {strip_size} -n {strip_name} {vg_name}'
        result = utils.exec_cmd(cmd, ssh_conn)
        return result

    # 创建mirror volume
    def create_mirror_volume(self, mirror_volume_size, data_volume_name, replica_volume_name, mirror_volume_name,
                             vg_name, ssh_conn=None):
        cmd = f'lvcreate -L {mirror_volume_size} -m1 -n {mirror_volume_name} {vg_name} {data_volume_name} {replica_volume_name}'
        result = utils.exec_cmd(cmd, ssh_conn)
        return result

    # 对thin pool进行扩容
    def extend_thin_pool(self, extend_sieze, thin_pool_name, ssh_conn=None):
        cmd = f'lvextend -L {extend_sieze} {thin_pool_name}'
        result = utils.exec_cmd(cmd, ssh_conn)
        return result

    # 对thin volume进行扩容
    def extend_thin_volume(self, extend_sieze, thin_volume_name, ssh_conn=None):
        cmd = f'lvextend -L {extend_sieze} {thin_volume_name}'
        result = utils.exec_cmd(cmd, ssh_conn)
        return result

    # 对thin volume进行缩减
    def reduce_thin_volume(self, extend_sieze, thin_volume_name, ssh_conn=None):
        cmd = f'lvreduce -L {extend_sieze} {thin_volume_name}'
        result = utils.exec_cmd(cmd, ssh_conn)
        return result

    # pv整体查看
    def check_pv(self, ssh_conn=None):
        cmd = f'pvs'
        result = utils.exec_cmd(cmd, ssh_conn)
        return result

    # pv查看详细
    def check_pv_detailed(self, pv_name, ssh_conn=None):
        cmd = f'pvdisplay {pv_name}'
        result = utils.exec_cmd(cmd, ssh_conn)
        return result

    # pv整盘扫描查看
    def check_pv_scan(self, ssh_conn=None):
        cmd = f'pvscan'
        result = utils.exec_cmd(cmd, ssh_conn)
        return result

    # vg整体查看
    def check_vg(self, ssh_conn=None):
        cmd = f'vgs'
        result = utils.exec_cmd(cmd, ssh_conn)
        return result

    # vg查看详细
    def check_vg_detailed(self, vg_name, ssh_conn=None):
        cmd = f'vgdisplay {vg_name}'
        result = utils.exec_cmd(cmd, ssh_conn)
        return result

    # vg整盘扫描查看
    def check_vg_scan(self, ssh_conn=None):
        cmd = f'vgscan'
        result = utils.exec_cmd(cmd, ssh_conn)
        return result

    # lv整体查看
    def check_lv(self, ssh_conn=None):
        cmd = f'lvs'
        result = utils.exec_cmd(cmd, ssh_conn)
        return result

    # lv查看详细
    def check_lv_detailed(self, lv_name, ssh_conn=None):
        cmd = f'lvdisplay {lv_name}'
        result = utils.exec_cmd(cmd, ssh_conn)
        return result

    # lv整盘扫描查看
    def check_lv_scan(self, ssh_conn=None):
        cmd = f'lvscan'
        result = utils.exec_cmd(cmd, ssh_conn)
        return result

    # pv删除
    def delete_pv(self, pv_name, ssh_conn=None):
        cmd = f'pvremove {pv_name}'
        result = utils.exec_cmd(cmd, ssh_conn)
        return result

    # vg删除
    def delete_vg(self, vg_name, ssh_conn=None):
        cmd = f'vgremove {vg_name}'
        result = utils.exec_cmd(cmd, ssh_conn)
        return result

    # lv删除
    def delete_lv(self, lv_name, ssh_conn=None):
        cmd = f'lvremove {lv_name}'
        result = utils.exec_cmd(cmd, ssh_conn)
        return result


class DISK(object):
    # 格式化disk
    def mkfs_disk(self, drbd_route, ssh_conn=None):
        cmd = f'mkfs.ext4 {drbd_route}'
        result = utils.exec_cmd(cmd, ssh_conn)
        return result

    # 挂载disk
    def mount_disk(self, drbd_route, ssh_conn=None):
        cmd = f'mount {drbd_route}/mnt'
        result = utils.exec_cmd(cmd, ssh_conn)
        return result

    # 卸载disk
    def umount_disk(self, drbd_route, ssh_conn=None):
        cmd = f'umount {drbd_route}'
        result = utils.exec_cmd(cmd, ssh_conn)
        return result
