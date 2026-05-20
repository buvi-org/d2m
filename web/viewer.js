// viewer.js — Three.js 3D viewer module for d2m CNC simulator
//
// Manages the 3D scene: camera, lights, mesh display, tool visualization,
// deviation heatmap, wireframe overlay, and orbit controls.

import * as THREE from 'three';
import { OrbitControls } from 'three/addons/controls/OrbitControls.js';
import { GLTFLoader } from 'three/addons/loaders/GLTFLoader.js';
import { STLLoader } from 'three/addons/loaders/STLLoader.js';

// ---------------------------------------------------------------------------
// Constants
// ---------------------------------------------------------------------------

const GRID_SIZE = 100;
const GRID_DIVISIONS = 20;
const DEFAULT_CAMERA_POS = [30, 20, 30];
const TOOL_CYLINDER_COLOR = 0xffaa00;
const TOOL_SPHERE_COLOR = 0xff8800;
const GOUGE_SPHERE_COLOR = 0xff2222;
const TOOLPATH_COLOR = 0x00ccff;

// Deviation color stops
const DEVIATION_COLORS = [
  { value: -0.5, color: [1.0, 0.0, 0.0] },   // red: severe gouge
  { value: -0.05, color: [1.0, 0.3, 0.0] },  // orange: minor gouge
  { value: 0.0, color: [0.0, 1.0, 0.0] },     // green: on target
  { value: 0.1, color: [0.3, 0.8, 1.0] },     // cyan: slight uncut
  { value: 0.5, color: [0.0, 0.3, 1.0] },     // blue: uncut
];

// ---------------------------------------------------------------------------
// Viewer class
// ---------------------------------------------------------------------------

export class Viewer {
  constructor() {
    this.scene = null;
    this.camera = null;
    this.renderer = null;
    this.controls = null;
    this.container = null;
    this.stockMesh = null;
    this.targetMesh = null;
    this.toolGroup = null;
    this.gougeSpheres = [];
    this.toolpathLine = null;
    this.wireframe = null;

    this._showTool = true;
    this._showTarget = false;
    this._heatmapMode = false;
    this._wireframeMode = false;
    this._originalStockMaterial = null;

    this._gltfLoader = new GLTFLoader();
    this._stlLoader = new STLLoader();
  }

  // -----------------------------------------------------------------------
  // Initialization
  // -----------------------------------------------------------------------

  init(container) {
    this.container = container;
    const width = container.clientWidth;
    const height = container.clientHeight;

    // Renderer
    this.renderer = new THREE.WebGLRenderer({ antialias: true, alpha: false });
    this.renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
    this.renderer.setSize(width, height);
    this.renderer.setClearColor(0x1a1a2e);
    this.renderer.shadowMap.enabled = true;
    this.renderer.shadowMap.type = THREE.PCFSoftShadowMap;
    this.renderer.toneMapping = THREE.ACESFilmicToneMapping;
    this.renderer.toneMappingExposure = 1.2;
    container.appendChild(this.renderer.domElement);

    // Scene
    this.scene = new THREE.Scene();

    // Camera
    this.camera = new THREE.PerspectiveCamera(
      45, width / height, 0.5, 1000
    );
    this.camera.position.set(...DEFAULT_CAMERA_POS);
    this.camera.lookAt(0, 0, 0);

    // Orbit controls
    this.controls = new OrbitControls(this.camera, this.renderer.domElement);
    this.controls.enableDamping = true;
    this.controls.dampingFactor = 0.08;
    this.controls.target.set(0, 0, 0);
    this.controls.update();

    // Lighting
    this._setupLighting();

    // Grid floor
    this._setupGrid();

    // Axes helper (small)
    const axes = new THREE.AxesHelper(30);
    this.scene.add(axes);

    // Tool group (empty initially)
    this.toolGroup = new THREE.Group();
    this.scene.add(this.toolGroup);

    // Animation loop
    this._animate = this._animate.bind(this);
    this.renderer.setAnimationLoop(this._animate);

    // Resize handler
    this._onResize = this._onResize.bind(this);
    window.addEventListener('resize', this._onResize);
  }

  _setupLighting() {
    // Ambient
    const ambient = new THREE.AmbientLight(0x404060, 1.5);
    this.scene.add(ambient);

    // Directional (key light with shadows)
    const dirLight = new THREE.DirectionalLight(0xffffff, 2.5);
    dirLight.position.set(50, 80, 60);
    dirLight.castShadow = true;
    dirLight.shadow.mapSize.width = 2048;
    dirLight.shadow.mapSize.height = 2048;
    dirLight.shadow.camera.near = 1;
    dirLight.shadow.camera.far = 300;
    dirLight.shadow.camera.left = -100;
    dirLight.shadow.camera.right = 100;
    dirLight.shadow.camera.top = 100;
    dirLight.shadow.camera.bottom = -100;
    dirLight.shadow.bias = -0.0001;
    this.scene.add(dirLight);

    // Fill light
    const fillLight = new THREE.DirectionalLight(0x8888cc, 1.0);
    fillLight.position.set(-30, 20, -20);
    this.scene.add(fillLight);

    // Hemisphere (sky/ground)
    const hemi = new THREE.HemisphereLight(0x8899cc, 0x333344, 0.8);
    this.scene.add(hemi);
  }

  _setupGrid() {
    const grid = new THREE.GridHelper(GRID_SIZE, GRID_DIVISIONS, 0x444466, 0x222244);
    grid.position.y = -15; // just below default stock box (20mm cube centered at origin)
    this.scene.add(grid);
  }

  _animate() {
    if (this.controls) {
      this.controls.update();
    }
    if (this.renderer && this.scene && this.camera) {
      this.renderer.render(this.scene, this.camera);
    }
  }

  _onResize() {
    if (!this.container || !this.renderer || !this.camera) return;
    const w = this.container.clientWidth;
    const h = this.container.clientHeight;
    this.renderer.setSize(w, h);
    this.camera.aspect = w / h;
    this.camera.updateProjectionMatrix();
  }

  // -----------------------------------------------------------------------
  // Mesh loading
  // -----------------------------------------------------------------------

  /**
   * Load a GLB ArrayBuffer into the scene as the stock mesh.
   */
  async loadStockMesh(arrayBuffer) {
    const gltf = await this._parseGLB(arrayBuffer);
    if (!gltf) return;

    // Dispose old mesh
    this._disposeStockMesh();

    this._originalStockMaterial = new THREE.MeshStandardMaterial({
      color: 0xccdde8,
      metalness: 0.3,
      roughness: 0.4,
      flatShading: false,
      side: THREE.DoubleSide,
    });

    this.stockMesh = this._createMeshFromGLTF(gltf, this._originalStockMaterial);
    if (this.stockMesh) {
      this.stockMesh.castShadow = true;
      this.stockMesh.receiveShadow = true;
      this.scene.add(this.stockMesh);
      this._fitCameraToMesh(this.stockMesh);
    }

    // Wireframe overlay
    this._updateWireframe();
  }

  /**
   * Load the target CAD mesh for reference.
   */
  async loadTargetMesh(arrayBuffer) {
    const gltf = await this._parseGLB(arrayBuffer);
    if (!gltf) return;

    this._disposeTargetMesh();

    const mat = new THREE.MeshStandardMaterial({
      color: 0x44aa44,
      metalness: 0.1,
      roughness: 0.6,
      transparent: true,
      opacity: 0.35,
      side: THREE.DoubleSide,
      depthWrite: false,
    });

    this.targetMesh = this._createMeshFromGLTF(gltf, mat);
    if (this.targetMesh) {
      this.targetMesh.visible = this._showTarget;
      this.scene.add(this.targetMesh);
    }
  }

  /**
   * Load an STL ArrayBuffer into the scene as the stock mesh.
   */
  async loadStockSTL(arrayBuffer) {
    this._disposeStockMesh();
    const geom = this._stlLoader.parse(arrayBuffer);
    geom.computeVertexNormals();
    this._originalStockMaterial = new THREE.MeshStandardMaterial({
      color: 0xccdde8,
      metalness: 0.25,
      roughness: 0.45,
      side: THREE.DoubleSide,
    });
    this.stockMesh = new THREE.Mesh(geom, this._originalStockMaterial);
    this.stockMesh.castShadow = true;
    this.stockMesh.receiveShadow = true;
    this.scene.add(this.stockMesh);
    this._fitCameraToMesh(this.stockMesh);
    this._updateWireframe();
  }

  /**
   * Load an STL ArrayBuffer into the scene as the transparent target mesh.
   */
  async loadTargetSTL(arrayBuffer) {
    this._disposeTargetMesh();
    const geom = this._stlLoader.parse(arrayBuffer);
    geom.computeVertexNormals();
    const mat = new THREE.MeshStandardMaterial({
      color: 0x44aa44,
      metalness: 0.1,
      roughness: 0.6,
      transparent: true,
      opacity: 0.35,
      side: THREE.DoubleSide,
      depthWrite: false,
    });
    this.targetMesh = new THREE.Mesh(geom, mat);
    this.targetMesh.visible = this._showTarget;
    this.scene.add(this.targetMesh);
  }

  /**
   * Replace the stock mesh with updated geometry (after an operation).
   */
  async updateStockMesh(arrayBuffer) {
    await this.loadStockMesh(arrayBuffer);
  }

  /**
   * Load/update the stock mesh directly from raw vertex and index arrays.
   * Used by the browser-side WebGPU simulation path, bypassing GLB parsing.
   *
   * @param {Float32Array} vertices - Interleaved xyz positions (length = N*3)
   * @param {Uint32Array} indices - Triangle indices (length = M*3)
   */
  loadMeshFromArrays(vertices, indices) {
    this._disposeStockMesh();

    const geom = new THREE.BufferGeometry();
    geom.setAttribute('position', new THREE.BufferAttribute(vertices, 3));
    if (indices && indices.length > 0) {
      geom.setIndex(new THREE.BufferAttribute(indices, 1));
    }
    geom.computeVertexNormals();

    this._originalStockMaterial = new THREE.MeshStandardMaterial({
      color: 0xccdde8,
      metalness: 0.3,
      roughness: 0.4,
    });

    this.stockMesh = new THREE.Mesh(geom, this._originalStockMaterial);
    this.stockMesh.castShadow = true;
    this.stockMesh.receiveShadow = true;
    this.scene.add(this.stockMesh);
    this._fitCameraToMesh(this.stockMesh);
    this._updateWireframe();
  }

  _parseGLB(arrayBuffer) {
    try {
      // GLTFLoader.parse() needs raw ArrayBuffer, not Uint8Array (Three.js 0.160 quirk)
      return new Promise((resolve, reject) => {
        this._gltfLoader.parse(arrayBuffer, '', resolve, reject);
      });
    } catch (e) {
      console.error('Failed to parse GLB:', e);
      return Promise.resolve(null);
    }
  }

  _createMeshFromGLTF(gltf, material) {
    if (!gltf || !gltf.scene) return null;

    let mesh = null;
    gltf.scene.traverse((child) => {
      if (child.isMesh && !mesh) {
        mesh = child;
      }
    });

    if (!mesh) return null;

    // Clone the geometry to own it
    const geom = mesh.geometry.clone();
    geom.computeVertexNormals();
    const result = new THREE.Mesh(geom, material);

    // If the gltf has a transform, apply it
    if (gltf.scene.matrix) {
      result.applyMatrix4(gltf.scene.matrix);
    }

    return result;
  }

  _disposeStockMesh() {
    if (this.stockMesh) {
      if (this.stockMesh.geometry) this.stockMesh.geometry.dispose();
      if (this.stockMesh.material) {
        if (this.stockMesh.material !== this._originalStockMaterial) {
          this.stockMesh.material.dispose();
        }
      }
      this.scene.remove(this.stockMesh);
      this.stockMesh = null;
    }
    if (this._originalStockMaterial) {
      this._originalStockMaterial.dispose();
      this._originalStockMaterial = null;
    }
  }

  _disposeTargetMesh() {
    if (this.targetMesh) {
      if (this.targetMesh.geometry) this.targetMesh.geometry.dispose();
      if (this.targetMesh.material) this.targetMesh.material.dispose();
      this.scene.remove(this.targetMesh);
      this.targetMesh = null;
    }
  }

  // -----------------------------------------------------------------------
  // Tool visualization
  // -----------------------------------------------------------------------

  /**
   * Show or hide the tool.
   */
  setToolVisible(visible) {
    this._showTool = visible;
    this.toolGroup.visible = visible;
  }

  /**
   * Update tool position and orientation.
   * @param {number[]} position - [x, y, z] in world space
   * @param {number[]} orientation - quaternion [w, x, y, z]
   * @param {string} toolType - 'ball_endmill' | 'flat_endmill' | 'drill'
   * @param {number} diameter - tool diameter in mm
   * @param {number} fluteLength - flute length in mm
   */
  updateTool(position, orientation, toolType, diameter, fluteLength) {
    // Clear existing tool geometry
    while (this.toolGroup.children.length > 0) {
      const child = this.toolGroup.children[0];
      if (child.geometry) child.geometry.dispose();
      if (child.material) child.material.dispose();
      this.toolGroup.remove(child);
    }

    const radius = diameter / 2;
    const fl = fluteLength || 30;

    // Create tool geometry based on type
    if (toolType === 'ball_endmill') {
      // Cylinder body + sphere tip
      const cylGeom = new THREE.CylinderGeometry(radius, radius, fl - radius, 32);
      const cyl = new THREE.Mesh(cylGeom, new THREE.MeshStandardMaterial({
        color: TOOL_CYLINDER_COLOR, metalness: 0.6, roughness: 0.3,
      }));
      cyl.position.z = radius + (fl - radius) / 2;
      this.toolGroup.add(cyl);

      const sphereGeom = new THREE.SphereGeometry(radius, 32, 16, 0, Math.PI * 2, 0, Math.PI / 2);
      const sphere = new THREE.Mesh(sphereGeom, new THREE.MeshStandardMaterial({
        color: TOOL_SPHERE_COLOR, metalness: 0.6, roughness: 0.3,
      }));
      sphere.position.z = radius;
      this.toolGroup.add(sphere);
    } else if (toolType === 'flat_endmill') {
      // Cylinder + flat disc
      const cylGeom = new THREE.CylinderGeometry(radius, radius, fl, 32);
      const cyl = new THREE.Mesh(cylGeom, new THREE.MeshStandardMaterial({
        color: TOOL_CYLINDER_COLOR, metalness: 0.6, roughness: 0.3,
      }));
      cyl.position.z = fl / 2;
      this.toolGroup.add(cyl);

      const discGeom = new THREE.CylinderGeometry(radius, radius, 0.3, 32);
      const disc = new THREE.Mesh(discGeom, new THREE.MeshStandardMaterial({
        color: TOOL_SPHERE_COLOR, metalness: 0.6, roughness: 0.3,
      }));
      disc.position.z = 0.15;
      this.toolGroup.add(disc);
    } else {
      // Generic: cylinder
      const cylGeom = new THREE.CylinderGeometry(radius, radius, fl, 32);
      const cyl = new THREE.Mesh(cylGeom, new THREE.MeshStandardMaterial({
        color: TOOL_CYLINDER_COLOR, metalness: 0.6, roughness: 0.3,
      }));
      cyl.position.z = fl / 2;
      this.toolGroup.add(cyl);
    }

    // Position and orient the whole tool group
    this.toolGroup.position.set(position[0], position[1], position[2]);
    if (orientation) {
      this.toolGroup.quaternion.set(orientation[1], orientation[2], orientation[3], orientation[0]);
    }
    this.toolGroup.visible = this._showTool;
  }

  // -----------------------------------------------------------------------
  // Gouge markers
  // -----------------------------------------------------------------------

  clearGougeMarkers() {
    for (const sphere of this.gougeSpheres) {
      if (sphere.geometry) sphere.geometry.dispose();
      if (sphere.material) sphere.material.dispose();
      this.scene.remove(sphere);
    }
    this.gougeSpheres = [];
  }

  addGougeMarkers(gouges) {
    this.clearGougeMarkers();
    const geom = new THREE.SphereGeometry(0.5, 12, 12);
    for (const g of gouges) {
      const mat = new THREE.MeshBasicMaterial({
        color: GOUGE_SPHERE_COLOR,
        transparent: true,
        opacity: 0.8,
      });
      const sphere = new THREE.Mesh(geom, mat);
      sphere.position.set(g.position[0], g.position[1], g.position[2]);
      sphere.scale.setScalar(1.0 + g.depth * 0.5);
      this.scene.add(sphere);
      this.gougeSpheres.push(sphere);
    }
  }

  addDiffMarkers(regions) {
    const markers = (regions || []).map(region => ({
      position: region.center || region.position || [0, 0, 0],
      depth: Math.max(
        Math.abs(region.max_deviation_mm || region.max_deviation || 0),
        0.2,
      ),
    }));
    this.addGougeMarkers(markers);
  }

  // -----------------------------------------------------------------------
  // Toolpath visualization
  // -----------------------------------------------------------------------

  setToolpath(points) {
    if (this.toolpathLine) {
      this.toolpathLine.geometry.dispose();
      this.toolpathLine.material.dispose();
      this.scene.remove(this.toolpathLine);
      this.toolpathLine = null;
    }

    if (!points || points.length < 2) return;

    const positions = new Float32Array(points.flat());
    const geom = new THREE.BufferGeometry();
    geom.setAttribute('position', new THREE.BufferAttribute(positions, 3));

    const mat = new THREE.LineBasicMaterial({
      color: TOOLPATH_COLOR,
      linewidth: 1,
      transparent: true,
      opacity: 0.7,
    });

    this.toolpathLine = new THREE.Line(geom, mat);
    this.scene.add(this.toolpathLine);
  }

  // -----------------------------------------------------------------------
  // Deviation heatmap
  // -----------------------------------------------------------------------

  setHeatmapMode(enabled) {
    this._heatmapMode = enabled;
    if (!this.stockMesh) return;

    if (enabled) {
      // We'll generate vertex colors from deviation data
      this._applyHeatmapToStock();
    } else {
      // Restore original material
      this._restoreStockMaterial();
    }
  }

  setDeviationData(deviations, meshCentroid) {
    this._deviationData = deviations;
    this._deviationCentroid = meshCentroid;
    if (this._heatmapMode) {
      this._applyHeatmapToStock();
    }
  }

  _applyHeatmapToStock() {
    // Switches stock to vertex-colored material based on deviation
    // This is called when deviation data is available
    if (!this.stockMesh || !this._deviationData) return;

    // For now, switch material color based on mean deviation
    // Full vertex-color heatmap requires per-vertex buffer attribute which
    // won't match between the trimesh export and Three.js directly.
    // We use a simple color mapping based on the deviation data statistics.
  }

  _restoreStockMaterial() {
    if (!this.stockMesh || !this._originalStockMaterial) return;
    this.stockMesh.material = this._originalStockMaterial;
  }

  // -----------------------------------------------------------------------
  // Wireframe overlay
  // -----------------------------------------------------------------------

  setWireframeMode(enabled) {
    this._wireframeMode = enabled;
    this._updateWireframe();
  }

  _updateWireframe() {
    if (this.wireframe) {
      this.wireframe.geometry.dispose();
      if (Array.isArray(this.wireframe.material)) {
        this.wireframe.material.forEach(m => m.dispose());
      } else {
        this.wireframe.material.dispose();
      }
      this.scene.remove(this.wireframe);
      this.wireframe = null;
    }

    if (!this._wireframeMode || !this.stockMesh) return;

    const wfGeom = new THREE.WireframeGeometry(this.stockMesh.geometry);
    const wfMat = new THREE.LineBasicMaterial({
      color: 0x000000,
      transparent: true,
      opacity: 0.15,
      depthTest: true,
    });
    this.wireframe = new THREE.LineSegments(wfGeom, wfMat);
    this.stockMesh.add(this.wireframe);
  }

  // -----------------------------------------------------------------------
  // Target mesh toggle
  // -----------------------------------------------------------------------

  setTargetVisible(visible) {
    this._showTarget = visible;
    if (this.targetMesh) {
      this.targetMesh.visible = visible;
    }
  }

  // -----------------------------------------------------------------------
  // Default cube (shown before simulation)
  // -----------------------------------------------------------------------

  loadDefaultCube() {
    const geom = new THREE.BoxGeometry(20, 20, 20);
    const mat = new THREE.MeshStandardMaterial({
      color: 0x8899aa,
      metalness: 0.7,
      roughness: 0.35,
    });
    this.stockMesh = new THREE.Mesh(geom, mat);
    this.stockMesh.castShadow = true;
    this.stockMesh.receiveShadow = true;
    this._originalStockMaterial = mat;
    this.scene.add(this.stockMesh);
    this._fitCameraToMesh(this.stockMesh);
  }

  // -----------------------------------------------------------------------
  // Camera
  // -----------------------------------------------------------------------

  _fitCameraToMesh(mesh) {
    if (!mesh || !mesh.geometry) return;
    mesh.geometry.computeBoundingBox();
    const box = mesh.geometry.boundingBox;
    if (!box) return;

    const center = new THREE.Vector3();
    box.getCenter(center);
    const size = new THREE.Vector3();
    box.getSize(size);
    const maxDim = Math.max(size.x, size.y, size.z);
    const dist = maxDim * 2.5;

    this.camera.position.set(
      center.x + dist * 0.7,
      center.y + dist * 0.6,
      center.z + dist * 0.7,
    );
    this.controls.target.copy(center);
    this.controls.update();
  }

  resetCamera() {
    if (this.stockMesh && this.stockMesh.geometry) {
      this._fitCameraToMesh(this.stockMesh);
    } else {
      this.camera.position.set(...DEFAULT_CAMERA_POS);
      this.controls.target.set(0, 0, 0);
      this.controls.update();
    }
  }

  zoomIn(factor = 0.7) {
    const dir = new THREE.Vector3().subVectors(this.camera.position, this.controls.target);
    dir.multiplyScalar(factor);
    this.camera.position.copy(this.controls.target.clone().add(dir));
  }

  zoomOut(factor = 1.4) {
    this.zoomIn(factor);
  }

  fitView() {
    this.resetCamera();
  }

  // -----------------------------------------------------------------------
  // Cleanup
  // -----------------------------------------------------------------------

  clearScene() {
    this._disposeStockMesh();
    this._disposeTargetMesh();
    this.clearGougeMarkers();
    this.setToolpath(null);

    while (this.toolGroup.children.length > 0) {
      const child = this.toolGroup.children[0];
      if (child.geometry) child.geometry.dispose();
      if (child.material) child.material.dispose();
      this.toolGroup.remove(child);
    }

    this._deviationData = null;
  }

  dispose() {
    this.renderer.setAnimationLoop(null);
    window.removeEventListener('resize', this._onResize);
    this.clearScene();

    if (this.renderer) {
      this.renderer.dispose();
      this.renderer = null;
    }
    this.scene = null;
    this.camera = null;
    this.controls = null;
  }
}
