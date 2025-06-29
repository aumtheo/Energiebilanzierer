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
          results.push({
            path: fullPath,
            size: stat.size,
            mtime: stat.mtime
          });
        }
      }
    } catch (error) {
      console.log(`Error accessing directory ${currentDir}: ${error.message}`);
    }
  }
  
  searchDirectory(dir);
  return results;
}

// Find all manage.py files in the Energiebilanz_Berechner directory
const startDir = process.argv[2] || '/home/project/Energiebilanz_Berechner';
const managePyFiles = findManagePy(startDir);

if (managePyFiles.length > 0) {
  console.log('Found manage.py files:');
  managePyFiles.forEach(file => {
    const mtime = file.mtime.toISOString().slice(0, 19).replace('T', ' ');
    console.log(`${file.size.toString().padStart(8)} bytes  ${mtime}  ${file.path}`);
  });
  
  console.log(`\nTotal: ${managePyFiles.length} manage.py files found`);
} else {
  console.log(`No manage.py files found in ${startDir}`);
}