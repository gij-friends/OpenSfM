import argparse
import sys
import subprocess


def clean(args):
    print('clean: ' + str(args))
    # docker停止
    subprocess.run("docker stop opensfm", shell=True)
    # opensfmimageに合致するイメージを削除
    subprocess.run("docker rmi $(docker images opensfmimage -q) -f", shell=True)
    # コンテナを削除
    subprocess.run('docker rm $(docker ps --filter name=opensfm --format "{{.ID}}" -a)', shell=True)


def init_docker(args):
    clean(args)
    hasUbuntu = subprocess.run(['docker', 'images', 'ubuntu', '-q'], capture_output=True, text=True)
    if not hasUbuntu.stdout:
        print('Ubuntuイメージが見つからないのでpullします')
        subprocess.run('docker pull ubuntu:20.04', shell=True)
    print('ビルド開始')
    subprocess.run("docker buildx build -t opensfmimage .", shell=True)
    print('ビルド完了')
    print('コンテナ作成')
    subprocess.run("docker run -it -d -p 8080:8080 --name opensfm opensfmimage", shell=True)


def run(args):
    if (args.all):
        clean(args)
        init_docker(args)
    subprocess.run(f'docker cp {args.data[0]} $(docker ps --filter name=opensfm -q):/source/OpenSfM/data/', shell=True)
    subprocess.run(f'docker exec -it opensfm bin/opensfm_run_all {args.data[0]}', shell=True)
    subprocess.run(f'docker exec -it opensfm bin/opensfm compute_depthmaps {args.data[0]}', shell=True)
    subprocess.run(f'docker cp $(docker ps --filter name=opensfm -q):/source/OpenSfM/{args.data[0]} data/', shell=True)


p = argparse.ArgumentParser(
    formatter_class=argparse.RawDescriptionHelpFormatter,
    description="""

# OpenSfMをDocker上で動作させるコマンドです

init で Dockerコンテナの起動までを行い、
-dオプションにデータの位置を指定すると点群の抽出を開始します

    """
)

# 引数を受け取る準備
group = p.add_mutually_exclusive_group()
subparser = p.add_subparsers()

# サブコマンド設定
parser_clean = subparser.add_parser("clean", help="作成したdocker環境を削除します")
parser_clean.set_defaults(handler=clean)

parser_init = subparser.add_parser("init", help="動かすための準備を行います")
parser_init.set_defaults(handler=init_docker)

# オプション設定
group.add_argument('-a', '--all', help='containerのビルド・作成から点群データの計算まで全て実行します', action='store_true')
group.add_argument('--bash', help='bashを起動してcontainer内に移動します', action='store_true')
p.add_argument('-d', '--data', metavar='DATA', help='(required) dataの階層 ex. data/berlin', type=str, nargs=1)
args = p.parse_args()

if hasattr(args, 'handler'):
    args.handler(args)
    sys.exit(0)
elif args.bash:
    subprocess.run("docker exec -it opensfm /bin/bash", shell=True)
    sys.exit(0)
elif args.data:
    print(args.data[0])
    run(args)
    sys.exit(0)
else: 
    p.print_help()
