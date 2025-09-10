label var hocvan Học_vấn
label var hocvan "Học vấn"
label def mgioitinh 1 "nam" 0 "nữ"
label def mchucvu 1 "nhân viên" 2 "trưởng nhóm" 3 "quản lý"
label dir
label list
label values gioitinh mgioitinh
sum luongthang
sum luongthang, detail
sum luongthang if chucvu == 3
tab chucvu, sum(luongthang)
table luongthang
tabstat luongthang, by (chucvu)
tabstat luongthang, s(n mean sd min max q) by (chucvu)

regress luongthang hocvan gioitinh thoigianlv truongnhom quanly
regress luongthang hocvan gioitinh thoigianlv truongnhom quanly, beta
scatter luongthang hocvan
scatter luongthang hocvan || lfit luongthang hocvan
scatter luongthang hocvan || qfit luongthang hocvan
correlate luongthang hocvan