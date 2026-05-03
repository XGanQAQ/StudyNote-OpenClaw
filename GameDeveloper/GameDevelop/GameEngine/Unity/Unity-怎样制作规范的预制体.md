```
PrefabName (根节点，放逻辑脚本 + Transform)
│
├── Model (美术模型 / Spine / FBX / Sprite / 特效)
│
├── Components (功能组件，如碰撞体、触发器、音效点、骨骼引用等)（如下）
├── Collider_Body         // 胶囊体 / BoxCollider
├── HitBox_Attack         // 攻击判定
├── HurtBox_Body          // 被击判定
├── Socket_Weapon         // 武器挂点
├── Audio_Footstep        // 脚步声
├── FX_SpawnPoint         // 特效释放点
└── Gizmo_Debug           // 画范围、调试

```