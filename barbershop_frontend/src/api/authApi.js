// src/api/authApi.js

// Dummy user data
const dummyUser = {
  id: 1,
  name: 'John Doe',
  email: 'john@example.com',
  password: 'password123' // password dummy
};

// Dummy login function
export const login = async ({ email, password }) => {
  // Simulasi delay server
  await new Promise(resolve => setTimeout(resolve, 500));

  if (email === dummyUser.email && password === dummyUser.password) {
    // Jika cocok, return objek sukses dengan user dan token dummy
    return {
      success: true,
      user: {
        id: dummyUser.id,
        name: dummyUser.name,
        email: dummyUser.email
      },
      token: 'dummy-jwt-token'
    };
  } else {
    // Jika tidak cocok, return gagal
    return {
      success: false
    };
  }
};
