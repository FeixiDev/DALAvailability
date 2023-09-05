
resource test2 {
    on vpxcosanj2 {
        device /dev/drbd1;
        disk /dev/sdb;
        address 10.20.30.40:7789;
        node-id 0;
        meta-disk internal;
    }
}
        