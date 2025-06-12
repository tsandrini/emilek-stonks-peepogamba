{ lib
, python312Packages
}:
python312Packages.buildPythonApplication {
  pname = "emilek-stonks-peepogamba";
  version = "0.1.0";

  src = ./.;
  pyproject = true;

  nativeBuildInputs = with python312Packages; [
    setuptools
  ];

  propagatedBuildInputs = with python312Packages; [
    requests
    yfinance
    protobuf
    curl-cffi
    websockets
  ];

  doCheck = false;

  meta = with lib; {
    description = "Hermetically reproducible gamba for our cute @widlarizer";
    license = licenses.mit;
    mainProgram = "emilek-stonks-peepogamba";
  };
}
