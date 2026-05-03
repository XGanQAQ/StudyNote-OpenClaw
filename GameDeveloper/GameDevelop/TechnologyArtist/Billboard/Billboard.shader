Shader "Unlit/Billboard"
{
    Properties
    {
        _MainTex ("Texture", 2D) = "white" {}
    }
    SubShader
    {
        Tags { "RenderType"="Opaque" }
        LOD 100

        Pass
        {
            CGPROGRAM
            #pragma vertex vert
            #pragma fragment frag
            // make fog work
            #pragma multi_compile_fog

            #include "UnityCG.cginc"

            struct appdata
            {
                float4 vertex : POSITION;
                float2 uv : TEXCOORD0;
            };

            struct v2f
            {
                float2 uv : TEXCOORD0;
                UNITY_FOG_COORDS(1)
                float4 vertex : SV_POSITION;
            };

            sampler2D _MainTex;
            float4 _MainTex_ST;

            float3 RecalculateAsBillboard(float3 ObjectPos)
            {
                float3 CameraPos = mul(unity_WorldToObject, float4(_WorldSpaceCameraPos, 1.0)).xyz;
                float3 CameraVector = normalize(CameraPos-ObjectPos);
                float3 tempUp = float3(0.0,1.0,0.0);

                float3 rightVector =  normalize(cross(CameraVector,tempUp));
                float3 upVector = normalize(cross(rightVector,CameraVector));

                float3 newPos = rightVector * ObjectPos.x +  upVector * ObjectPos.y + CameraVector * ObjectPos.z;
                
                return  newPos;
            }

            v2f vert (appdata v)
            {
                v2f o;
                
                float3 pos = RecalculateAsBillboard(v.vertex);
                
                o.vertex = UnityObjectToClipPos(pos);
                o.uv = TRANSFORM_TEX(v.uv, _MainTex);
                UNITY_TRANSFER_FOG(o,o.vertex);
                return o;
            }

            fixed4 frag (v2f i) : SV_Target
            {
                // sample the texture
                fixed4 col = tex2D(_MainTex, i.uv);
                // apply fog
                UNITY_APPLY_FOG(i.fogCoord, col);
                return col;
            }
            ENDCG
        }
    }
}
