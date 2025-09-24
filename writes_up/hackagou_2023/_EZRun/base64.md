Encode généralement utilisé dans les CTF. La majeure partie fini par ou/des signe ‘=’ mais ce n’est pas une obligation.

Pour les décoder :
* [cyberchef](../../../../ressouces/tools/cyberchef.md) : https://gchq.github.io/CyberChef/#recipe=From_Base64('A-Za-z0-9%2B/%3D',true,false)
* bash
```bash
echo "STRING" | base64 -d
```
