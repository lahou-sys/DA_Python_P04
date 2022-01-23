from controllers.launcher import LauncherController


class Main:
    def perform(self):
        launcher = LauncherController()
        launcher.banner()
        launcher.perform()


if __name__ == "__main__":
    main = Main()
    main.perform()
