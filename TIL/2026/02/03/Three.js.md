# Three.js

> 날짜: 2026-02-03
> 원본 노션: [링크](https://www.notion.so/Three-js-2fcb28703eb080f9a93df2a2aa704493)

---

# ArcballControls.js

마우스로 3D 오브젝트를 회전·이동·줌

# DragControls.js

new DragControls(objects, camera, renderer.domElement);

오브젝트를 직접 드래그

- 마우스로 Mesh를 끌어서 이동
- 카메라는 안 움직임
- 선택한 오브젝트만 이동
- OrbitControls와 같이 쓰면 충돌 → on/off 필요
- 블럭 이동 
# FirstPersonControls.js

1인칭 시점 카메라

- 마우스: 시점 회전
- WASD: 이동
- 중력 없음
# FlyControls.js

완전 자유 비행 (6 DOF)

- 위/아래/앞/뒤/좌/우 + 회전
- 비행기·우주선 느낌
- 방향 제한 없음
- movementSpeed 
- rollSpeed
# MapControls.js

지도 스타일 이동

- 회전 제한 (위에서 내려다보는 시점)
- Z축 회전만 허용
- 좌우 이동(Pan) 중심
# OrbitControls.js

controls.target.set(0, 0, 0);

대상 주위를 회전

- 줌 / 팬 가능
# PointerLockControls.js

# TrackballControls.js

# TransformControls.js

controls.setMode("translate"); // rotate, scale

오브젝트 변형 전용

- 이동 / 회전 / 크기 조절
- Gizmo 표시 (축 화살표)
