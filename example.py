from dfs import Mason
import control

# declares some gains
tf_actuator = control.ss2tf(-24, 24, 1, 0) 	# A state space object
float_gain = 0.00140293442430542 			# A float gain
integrator = control.tf([1], [1, 0])		# A Transger Function object

# ======================================================================================================================
# Construct a system

mySystem = Mason('mySystem')
mySystem.create_node('Input', 'I')
mySystem.create_node('actuator')
mySystem.connect_node('Input', 'actuator', tf_actuator)
mySystem.create_node('alpha')
mySystem.connect_node('actuator', 'alpha', float_gain)
node_name = mySystem.create_node()
mySystem.connect_node('alpha', node_name, theta)
mySystem.create_node('output', 'O')
mySystem.connect_node(node_name, 'output', integrator)
tf_mySystem = mySystem.get_sis_tf()

# ======================================================================================================================
# Output is a Transger Function object, once that one of the gais was of this type. See the library "python-control"
# If all the gains was float, the output would be float

print(tf_mySystem.minreal())
