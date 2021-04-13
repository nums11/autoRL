const express = require('express');
const { spawn } = require('child_process');
const { PythonShell } = require('python-shell')
const cors = require('cors');
const bodyParser = require('body-parser');
const options = { 
  mode: 'text', 
  pythonOptions: ['-u'], // get print results in real-time 
  args: []
}; 

const app = express();
app.use(cors({
  origin: 'http://localhost:8080',
  methods:['POST'],
  credentials:true, 
}))
app.use(bodyParser.urlencoded({ extended: true }));
app.use(bodyParser.json());

app.post('/train', function (req, res) {
	const algo_num = req.body.algo_num
	const state_space_size = req.body.state_space_size
	const action_space_size = req.body.action_space_size
	const algo = getAlgo(algo_num)
	options.args = [algo, state_space_size, action_space_size]
	PythonShell.run('scripts/train.py', options, function(error, result) {
		if(error) throw error
		// const rent = result[0]
		// console.log(`Sending rent ${rent}`)
		console.log("Returned from script", result)
		res.json(result)
	})
})

function getAlgo(algo_num) {
	if(algo_num == '1')
		return 'q_learning'
	else if(algo_num == '2')
		return 'monte_carlo'
	else if(algo_num == '3')
		return 'sarsa'
	else if(algo_num == '4')
		return 'double_q_learning'
	else if(algo_num == '5')
		return 'n_step_sarsa'
	else if(algo_num == '6')
		return 'expected_sarsa'
}

app.listen(4000, () => console.log('Application listening on port 4000!'))