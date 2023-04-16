## 追記

### docker動かし方

ビルドはbuildXを使えるようにしておいて
```
docker buildx build -t opensfmimage .
```

コンテナ作成

```
docker run -it -d --mount type=bind,source="$(pwd)"/data,target=/source/OpenSfm/data  -p 8080:8080 --name opensfm opensfmimage
```

bash起動
```
docker exec -it opensfm /bin/bash
```

containerId取得(停止中は -a つけないと取得できない)
```
docker ps --filter name=opensfm --format "{{.ID}}" -a
```

データコピー
(host -> container)

```
docker cp data/ "$(docker ps --filter name=opensfm --format "{{.ID}}" -a)":/source/OpenSfM/
```

(container -> host)
```
docker cp "$(docker ps --filter name=opensfm --format "{{.ID}}" -a)":/source/OpenSfM/data .
```

コンテナ削除
```
docker rm "$(docker ps --filter name=opensfm --format "{{.ID}}" -a)"
```
----


OpenSfM ![Docker workflow](https://github.com/mapillary/opensfm/workflows/Docker%20CI/badge.svg)
=======

## Overview
OpenSfM is a Structure from Motion library written in Python. The library serves as a processing pipeline for reconstructing camera poses and 3D scenes from multiple images. It consists of basic modules for Structure from Motion (feature detection/matching, minimal solvers) with a focus on building a robust and scalable reconstruction pipeline. It also integrates external sensor (e.g. GPS, accelerometer) measurements for geographical alignment and robustness. A JavaScript viewer is provided to preview the models and debug the pipeline.

<p align="center">
  <img src="https://opensfm.org/docs/_images/berlin_viewer.jpg" />
</p>

Checkout this [blog post with more demos](http://blog.mapillary.com/update/2014/12/15/sfm-preview.html)


## Getting Started

* [Building the library][]
* [Running a reconstruction][]
* [Documentation][]


[Building the library]: https://opensfm.org/docs/building.html (OpenSfM building instructions)
[Running a reconstruction]: https://opensfm.org/docs/using.html (OpenSfM usage)
[Documentation]: https://opensfm.org/docs/ (OpenSfM documentation)

## License
OpenSfM is BSD-style licensed, as found in the LICENSE file.  See also the Facebook Open Source [Terms of Use][] and [Privacy Policy][]

[Terms of Use]: https://opensource.facebook.com/legal/terms (Facebook Open Source - Terms of Use)
[Privacy Policy]: https://opensource.facebook.com/legal/privacy (Facebook Open Source - Privacy Policy)
