const { exec } = require('child_process');

exec('python test.py', (err, stdout, stderr) => {
  if (err) {
    //some err occurred
    console.error(err);
  } else {
   // the *entire* stdout and stderr (buffered)
   console.log(`stdout: ${stdout}`);
   console.log(`stderr: ${stderr}`);
  }
});
