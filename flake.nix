{
  description = "Development environment for roombapy";

  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";
  };

  outputs =
    { self, nixpkgs }:
    let
      systems = [
        "x86_64-linux"
        "aarch64-linux"
        "x86_64-darwin"
        "aarch64-darwin"
      ];
      forEachSystem = nixpkgs.lib.genAttrs systems;
    in
    {
      devShells = forEachSystem (
        system:
        let
          pkgs = nixpkgs.legacyPackages.${system};
        in
        {
          default = pkgs.mkShell {
            packages = with pkgs; [
              uv
              python313
              mosquitto
            ];

            env = {
              UV_PYTHON_PREFERENCE = "only-system";
            };

            shellHook = ''
              echo "roombapy dev shell (uv $(uv --version))"
              uv sync --all-extras --dev
            '';
          };
        }
      );
    };
}
