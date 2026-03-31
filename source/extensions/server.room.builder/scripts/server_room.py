import omni.ext
import omni.usd
import asyncio
from pxr import UsdGeom, Gf


print("FILE LOADED 🚀")  # DEBUG


class ServerRoomExtension(omni.ext.IExt):

    def on_startup(self, ext_id):
        print("🔥 EXTENSION STARTED")
        asyncio.ensure_future(self.setup_scene())

    async def setup_scene(self):
        context = omni.usd.get_context()

        # Create new stage
        context.new_stage()

        while not context.get_stage():
            await asyncio.sleep(0.1)

        print("✅ Stage ready")

        stage = context.get_stage()
        self.create_scene(stage)

    def create_scene(self, stage):

        print("🚀 Creating cube...")

        # Create world
        world = stage.DefinePrim("/World", "Xform")
        stage.SetDefaultPrim(world)

        # Create cube
        cube = UsdGeom.Cube.Define(stage, "/World/Cube")
        cube.CreateSizeAttr(2)
        cube.AddTranslateOp().Set(Gf.Vec3f(0, 0, 1))

        print("✅ Cube created!")