import trimesh
import numpy as np

# hand_link

# Load the original STL file
mesh = trimesh.load_mesh("assets/meshes/hand_link.STL")

# Mirror across X-axis (YZ plane): scale X by -1
mirror_matrix = np.diag([1, 1, -1, 1])  # homogeneous transform
mesh.apply_transform(mirror_matrix)

# Save to new file
mesh.export("hand_link_left.stl")

print("Mirrored STL saved as 'hand_link_left.stl'")


# mcp_joint

# Load the original STL file
mesh_1 = trimesh.load_mesh("assets/meshes/mcp_joint.stl")

# Mirror across X-axis (YZ plane): scale X by -1
mirror_matrix = np.diag([1, 1, -1, 1])  # homogeneous transform
mesh_1.apply_transform(mirror_matrix)

# Save to new file
mesh_1.export("mcp_joint_left.stl")

print("Mirrored STL saved as 'mcp_joint_left.stl'")