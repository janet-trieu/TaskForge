import config from './config.json';

const URL = `http://localhost:${config.BACKEND_PORT}`;

export const makeRequest = async (path, method, body, uid) => {
  if (body) {
    if (method === 'GET') {
      const response = await fetch(`${URL}${path}?` + new URLSearchParams(body), {
        method,
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `${uid}`,
        }
      });
      const data = await response.json();
      return data;
    } else {
      const response = await fetch(`${URL}${path}`, {
        method,
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `${uid}`,
        },
        body: JSON.stringify(body)
      });
      const data = await response.json();
      return data;
    }
  } else {
    const response = await fetch(`${URL}${path}`, {
      method,
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `${uid}`,
      }
    });
    const data = await response.json();
    return data;
  }
}

export const fileToDataUrl = (file) => {
  if (!file) return;

  const validFileTypes = ['image/jpeg', 'image/png', 'image/jpg']
  const valid = validFileTypes.find(type => type === file.type);

  // Bad data, let's walk away.
  if (!valid) {
    alert('Provided file is not a png, jpg, or jpeg image.');
    return null;
  }

  const reader = new FileReader();
  const dataUrlPromise = new Promise((resolve, reject) => {
    reader.onerror = reject;
    reader.onload = () => resolve(reader.result);
  });
  reader.readAsDataURL(file);
  return dataUrlPromise;
}

