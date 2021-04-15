const express = require('express');
const { spawn } = require('child_process');
const { PythonShell } = require('python-shell')
const cors = require('cors');
const bodyParser = require('body-parser');
const fs = require('fs');
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
	const env_name = req.body.env_name
	const episode_sets = req.body.episode_sets
	const algo_num = req.body.algo_num
	const algo = getAlgo(algo_num)
	const n = req.body.n
	const learning_rate = req.body.learning_rate
	const epsilon = req.body.epsilon
	const min_epsilon = req.body.min_epsilon
	const epsilon_decay_rate = req.body.epsilon_decay_rate
	const discount_factor = req.body.discount_factor
	const max_steps_per_episode = req.body.max_steps_per_episode

	options.args = [env_name, algo, n, learning_rate, epsilon,
	min_epsilon, epsilon_decay_rate, discount_factor,
	max_steps_per_episode, episode_sets.length]
	episode_sets.forEach(set => { options.args.push(set) })

	const shell = new PythonShell('scripts/train.py', options)
	const final_output = []
	let store_output = false
	shell.on('message', function(message) {
		console.log(message)
		if(message === 'Beginning Training')
			store_output = false
		if(store_output)
			final_output.push(message)
		if(message === 'Done Training')
			store_output = true
	})
	shell.on('stderr', function(error) {
		console.log("Received error")
		throw error
	})
	shell.end(function(error, code, signal) {
		console.log("Shell ended")
		if(error) throw error
		console.log("code", code)
		console.log("signal", signal)
		res.json(final_output)
	})
})

app.get('/policy_names', function(req, res) {
	const folder_name = './policies/'
	const policy_names = []
	fs.readdirSync(folder_name).forEach(file => {
	  policy_names.push(file)
	});
	res.json(policy_names)
})

app.post('/test', function (req, res) {
	const env_name = req.body.env_name
	const num_testing_episodes = req.body.num_testing_episodes
	const policies = req.body.policies
	options.args = [env_name, num_testing_episodes, policies.length]
	policies.forEach(policy => { options.args.push(policy) })
	const shell = new PythonShell('scripts/test.py', options)
	const final_output = []
	let store_output = false
	shell.on('message', function(message) {
		console.log(message)
		if(message === 'Beginning Testing')
			store_output = false
		if(store_output)
			final_output.push(message)
		if(message === 'Done Testing')
			store_output = true
	})
	shell.on('stderr', function(error) {
		console.log("Received error")
		throw error
	})
	shell.end(function(error, code, signal) {
		console.log("Shell ended")
		if(error) throw error
		console.log("code", code)
		console.log("signal", signal)
		res.json(final_output)
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