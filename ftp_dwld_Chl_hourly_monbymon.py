from ftplib import FTP
import calendar
import os

def get_days(year, month):
    information = calendar.monthrange(year, month)
    return list(range(1, information[-1] + 1))

def download_files(ftp, local_directory, remote_directory, file_extension):
    ftp.cwd(remote_directory)
    files = ftp.nlst()
    files.sort()

    for file in files[:]:
        if file.endswith(file_extension):
            file_path = os.path.join(local_directory, file)
            with open(file_path, 'wb') as file_handle:
                ftp.retrbinary(f'RETR {file}', file_handle.write)

def download_files_for_year(ftp, local_root, remote_root, year):
    for month in range(1, 13):
        start_day = 1
        end_day = calendar.monthrange(year, month)[1]

        local_directory = os.path.join(local_root, str(year), f'{month:02}')
        remote_directory = f"/pub/himawari/L3/CHL/021/{year}{month:02}"

        if not os.path.exists(local_directory):
            os.makedirs(local_directory)

        download_files(ftp, local_directory, remote_directory, '02401.nc')

def main():
    ftp = FTP()
    ftp.set_debuglevel(2)
    ip = "ftp.ptree.jaxa.jp"
    port = 21
    user = "yuxingban_gmail.com"
    password = "SP+wari8"

    ftp.connect(ip, port)
    ftp.login(user, password)

    local_root = '/Users/byxxx/Documents/srdp Chl/himawari/hourly'  # 修改为你本地的根目录
    remote_root = "/pub/himawari/L3/CHL/021"

    year = 2021
    download_files_for_year(ftp, local_root, remote_root, year)

    ftp.set_debuglevel(0)
    ftp.quit()

if __name__ == "__main__":
    main()
