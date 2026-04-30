import React, { useEffect, useRef } from 'react'
import * as THREE from 'three'
import './Avatar.css'

function Avatar({ agentInfo }) {
  const containerRef = useRef(null)
  const sceneRef = useRef(null)
  const cameraRef = useRef(null)
  const rendererRef = useRef(null)

  useEffect(() => {
    initializeScene()

    return () => {
      if (rendererRef.current && containerRef.current) {
        containerRef.current.removeChild(rendererRef.current.domElement)
      }
    }
  }, [])

  const initializeScene = () => {
    if (!containerRef.current) return

    // Scene setup
    const scene = new THREE.Scene()
    scene.background = new THREE.Color(0x1e293b)
    sceneRef.current = scene

    // Camera setup
    const width = containerRef.current.clientWidth
    const height = containerRef.current.clientHeight
    const camera = new THREE.PerspectiveCamera(75, width / height, 0.1, 1000)
    camera.position.z = 5
    cameraRef.current = camera

    // Renderer setup
    const renderer = new THREE.WebGLRenderer({ antialias: true })
    renderer.setSize(width, height)
    renderer.setPixelRatio(window.devicePixelRatio)
    containerRef.current.appendChild(renderer.domElement)
    rendererRef.current = renderer

    // Lighting
    const ambientLight = new THREE.AmbientLight(0xffffff, 0.8)
    scene.add(ambientLight)

    const pointLight = new THREE.PointLight(0xffffff, 0.5)
    pointLight.position.set(10, 10, 10)
    scene.add(pointLight)

    // Create a simple animated cube placeholder
    createPlaceholderAvatar(scene)

    // Animation loop
    const animate = () => {
      requestAnimationFrame(animate)
      renderer.render(scene, camera)
    }
    animate()

    // Handle window resize
    const handleResize = () => {
      const newWidth = containerRef.current?.clientWidth || width
      const newHeight = containerRef.current?.clientHeight || height
      camera.aspect = newWidth / newHeight
      camera.updateProjectionMatrix()
      renderer.setSize(newWidth, newHeight)
    }
    window.addEventListener('resize', handleResize)

    return () => window.removeEventListener('resize', handleResize)
  }

  const createPlaceholderAvatar = (scene) => {
    // Create a simple cube as placeholder
    const geometry = new THREE.BoxGeometry(2, 3, 1)
    const material = new THREE.MeshPhongMaterial({
      color: 0x6366f1,
      shininess: 100
    })
    const cube = new THREE.Mesh(geometry, material)
    scene.add(cube)

    // Animate rotation
    const animate = () => {
      cube.rotation.x += 0.005
      cube.rotation.y += 0.01
    }

    // Store animation function for cleanup if needed
    scene.userData.animate = animate
  }

  return (
    <div className="avatar-container">
      <div ref={containerRef} className="avatar-viewport" />
      <div className="avatar-info">
        <h2>{agentInfo?.name || 'Agent'}</h2>
        <p className="personality">{agentInfo?.personality}</p>
      </div>
    </div>
  )
}

export default Avatar
