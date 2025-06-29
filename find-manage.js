const fs = require('fs');
const path = require('path');

function findManagePy(dir) {
  const results = [];
  
  function searchDirectory(currentDir) {
    try {
      const items = fs.readdirSync(currentDir);
      
      for (const item of items) {
        const fullPath = path.join(currentDir, item);
        const stat = fs.statSync(fullPath);
        
        if (stat.isDirectory()) {
          searchDirectory(fullPath);
        } else if (item === 'manage.py') {
          results.push(fullPath);
        }
      }
    } catch (error) {
      // Skip directories we can't read
    }
  }
  
  searchDirectory(dir);
  return results;
}

// Find all manage.py files in the Energiebilanz_Berechner directory
const managePyFiles = findManagePy('/home/project/Energiebilanz_Berechner');

if (managePyFiles.length > 0) {
  console.log('Found manage.py files:');
  managePyFiles.forEach(file => {
    try {
      const stat = fs.statSync(file);
      const permissions = stat.mode.toString(8).slice(-3);
      const size = stat.size;
      const mtime = stat.mtime.toISOString().slice(0, 19).replace('T', ' ');
      
      console.log(`-rw-r--r-- 1 user user ${size.toString().padStart(8)} ${mtime} ${file}`);
    } catch (error) {
      console.log(`Error reading stats for ${file}: ${error.message}`);
    }
  });
} else {
  console.log('No manage.py files found in /home/project/Energiebilanz_Berechner');
}