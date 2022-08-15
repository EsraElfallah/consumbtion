import time
import psutil
import csv


def get_size(bytes):
    for unit in ['B', 'KB', 'MB', 'GB', 'TB', 'PB']:
        if bytes < 1024:
            return f'{bytes:.2f}{unit}'
        else:
            bytes = bytes / 1024


last_rec = psutil.net_io_counters().bytes_recv
last_sent = psutil.net_io_counters().bytes_sent
last_total = last_rec + last_sent

bytes_rec = 0
bytes_sent = 0
bytes_total = 0

now_rec = 0
now_sent = 0
now_total = 0

old_data_rec = 0
old_data_sent = 0
old_data_total = 0

starter = 0

print(
    f"#######fixed first down {get_size(last_rec)} fixed first upload {get_size(last_sent)} fixed first total{get_size(last_total)}#####")
with open("segma.csv", "a") as wt:
    csv_w = csv.DictWriter(wt,
                           fieldnames=['downCon', 'uplaodCon', 'totalCon', 'first down', 'first upload', 'first total',
                                       'bytes down', 'bytes up', 'bytes total', 'old rec', 'old sent', 'hyper', 'segma', 'now down', 'now sent', 'now total'])
    csv_w.writeheader()

    while True:
        # debug
        hyper = 0
        segma = 0
        if starter == 0 and psutil.net_io_counters().bytes_recv != 0:
            bytes_rec = psutil.net_io_counters().bytes_recv
        elif starter == 0 and psutil.net_io_counters().bytes_recv == 0:
            bytes_rec = last_rec

        if starter == 0 and psutil.net_io_counters().bytes_sent != 0:
            bytes_sent = psutil.net_io_counters().bytes_sent
        elif starter == 0 and psutil.net_io_counters().bytes_sent == 0:
            bytes_sent = last_sent

        bytes_total = bytes_rec + bytes_sent

        starter = 1

        if psutil.net_io_counters().bytes_recv == 0:
            old_data_rec += bytes_rec
            old_data_sent += bytes_sent
            hyper = 1
        elif psutil.net_io_counters().bytes_sent == 0:
            old_data_rec += bytes_rec
            old_data_sent += bytes_sent
            segma = 1


        old_data_total = old_data_rec + old_data_sent



        bytes_rec = psutil.net_io_counters().bytes_recv
        bytes_sent = psutil.net_io_counters().bytes_sent
        bytes_total = bytes_rec + bytes_sent

        now_rec = bytes_rec
        now_sent = bytes_sent
        now_total = bytes_total


        now_rec += old_data_rec
        now_sent += old_data_sent
        now_total += old_data_total

        print(f"-----> new to current second  down {get_size(bytes_rec)} upload {get_size(bytes_sent)}  total{get_size(bytes_total)} old{old_data_rec} hyper{hyper}")

        new_rec = now_rec - last_rec
        new_sent = now_sent - last_sent
        new_total = now_total - last_total

        print(
            f"-----> consuption each second  down {get_size(new_rec)} upload {get_size(new_sent)}  total{get_size(new_total)}")
        mb_rec = get_size(new_rec)
        mb_sent = get_size(new_sent)
        mb_total = get_size(new_total)



        csv_w.writerow(
            {
                'downCon': mb_rec,
                'uplaodCon': mb_sent,
                'totalCon': mb_total,
                'first down': {get_size(last_rec)},
                'first upload': {get_size(last_sent)},
                'first total': {get_size(last_total)},
                'bytes down': {get_size(bytes_rec)},
                'bytes up': {get_size(bytes_sent)},
                'bytes total': {get_size(bytes_total)},
                'now down': now_rec,
                'now sent': now_sent,
                'now total': now_total,
                'old rec': old_data_rec,
                'old sent': old_data_sent,
                'hyper': hyper,
                'segma': segma

            }
        )
        wt.flush()

        print(f"#######DownloadCon: {mb_rec}  UploadCon: {mb_sent}  TotalCon: {mb_total}")

        time.sleep(1)

