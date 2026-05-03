```cs
using UnityEngine;  
  
namespace Gameplay.Player  
{  
    /// <summary>  
    /// 通用第一人称射线检测，获取玩家注视的 GameObject。  
    /// </summary>  
    public class FirstPersonRaycaster : MonoBehaviour  
    {  
        [Header("Raycast Settings")]  
        [SerializeField] private float rayLength = 15f;  
        [SerializeField] private LayerMask layerMask = ~0; // 默认检测所有层  
        [SerializeField] private Camera playerCamera;  
        [SerializeField] private bool drawGizmos = true;  
  
        /// <summary>  
        /// 当前玩家注视的 GameObject（只读）。  
        /// </summary>  
        public GameObject CurrentLookAtObject { get; private set; }  
  
        void Awake()  
        {            if (playerCamera == null)  
            {                var camObj = GameObject.FindWithTag("MainCamera");  
                if (camObj != null)  
                    playerCamera = camObj.GetComponent<Camera>();  
            }        }  
        void Update()  
        {            UpdateLookAtObject();  
        }  
        private void UpdateLookAtObject()  
        {            if (playerCamera == null)  
            {                CurrentLookAtObject = null;  
                return;  
            }            Ray ray = new Ray(playerCamera.transform.position, playerCamera.transform.forward);  
            if (Physics.Raycast(ray, out RaycastHit hit, rayLength, layerMask))  
            {                CurrentLookAtObject = hit.collider.gameObject;  
            }            else  
            {  
                CurrentLookAtObject = null;  
            }        }  
        void OnDrawGizmos()  
        {            if (!drawGizmos) return;  
            Camera cam = playerCamera;  
            if (cam == null && Application.isPlaying == false)  
            {                var camObj = GameObject.FindWithTag("MainCamera");  
                if (camObj != null)  
                    cam = camObj.GetComponent<Camera>();  
            }            if (cam == null) return;  
            Gizmos.color = Color.cyan;  
            Vector3 origin = cam.transform.position;  
            Vector3 dir = cam.transform.forward * rayLength;  
            Gizmos.DrawLine(origin, origin + dir);  
        }    }}
```