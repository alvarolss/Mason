# Mason
Mason's Gain Rule implementation. This library is responsible for generating the object that will store the system to be created. The class structure is shown in the table below:

<table>
  <tr>
    <th>Function</th>
    <th>parameters</th>
    <th>Return</th>
  </tr>
  <tr>
    <td>__init__</td>
    <td>Name (optional): string / integer</td>
    <td>Object</td>
  </tr>
  <tr>
    <td>create_node</td>
    <td>Name (optional): string / integer;<br> Input/Output (optional): string / integer</td>
    <td>String</td>
  </tr>
  <tr>
    <td>set_input</td>
    <td>Name (optional): string / integer</td>
    <td>Boolean</td>
  </tr>
  <tr>
    <td>get_input</td>
    <td>-</td>
    <td>String</td>
  </tr>
  <tr>
    <td>set_output</td>
    <td>Name (optional): string / integer</td>
    <td>Boolean</td>
  </tr>
  <tr>
    <td>output</td>
    <td>-</td>
    <td>String</td>
  </tr>
  <tr>
    <td>connect_node</td>
    <td>Input node name: string / integer;<br>Output node name: string / integer;<br>Gain (optional): float / control.TransferFunction</td>
    <td>Boolean</td>
  </tr>
  <tr>
    <td>get_sis_tf</td>
    <td>-</td>
    <td>Depends on the gains types</td>
  </tr>
</table>
