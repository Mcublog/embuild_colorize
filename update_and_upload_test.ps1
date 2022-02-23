Remove-Item	dist -Recurse -Force -Confirm:$false
py -m build
py -m twine upload --repository testpypi dist/*