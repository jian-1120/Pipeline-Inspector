"""Check registry. Single source of check ordering."""

from . import materials, normals, textures, transforms, uvs

CHECK_REGISTRY = (
    (textures.CHECK_ID, textures.CHECK_NAME, textures.run),
    (materials.CHECK_ID, materials.CHECK_NAME, materials.run),
    (transforms.CHECK_ID, transforms.CHECK_NAME, transforms.run),
    (uvs.CHECK_ID, uvs.CHECK_NAME, uvs.run),
    (normals.CHECK_ID, normals.CHECK_NAME, normals.run),
)
