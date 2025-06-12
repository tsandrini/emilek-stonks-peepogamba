# --- flake-parts/pkgs/default.nix
{ ... }:
{
  perSystem =
    { config, pkgs, ... }:
    {
      packages = {
        # NOTE For more info on the nix `callPackage` pattern see
        # https://nixos.org/guides/nix-pills/13-callpackage-design-pattern.html
        default = config.packages.emilek-stonks-peepogamba;

        emilek-stonks-peepogamba = pkgs.callPackage ./emilek-stonks-peepogamba { };
      };
    };
}
