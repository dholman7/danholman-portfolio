// Mock API functions for testing
// eslint-disable-next-line @typescript-eslint/no-unused-vars
const mockRegister = async (data: Record<string, unknown>) => {
  await new Promise(resolve => setTimeout(resolve, 100));
  
  if (Math.random() > 0.1) {
    return { success: true, message: 'Account created successfully!' };
  } else {
    return { success: false, message: 'Email already exists. Please try a different email.' };
  }
};

// eslint-disable-next-line @typescript-eslint/no-unused-vars
const mockLogin = async (email: string, password: string) => {
  await new Promise(resolve => setTimeout(resolve, 100));
  
  if (Math.random() > 0.2) {
    return { success: true, message: 'Login successful!' };
  } else {
    return { success: false, message: 'Invalid email or password.' };
  }
};

describe('Mock API Functions', () => {
  describe('mockRegister', () => {
    it('should return a response with success property', async () => {
      const testData = {
        firstName: 'John',
        lastName: 'Doe',
        email: 'john@example.com',
        password: 'password123',
        confirmPassword: 'password123',
        terms: true
      };

      const result = await mockRegister(testData);
      
      expect(result).toHaveProperty('success');
      expect(result).toHaveProperty('message');
      expect(typeof result.success).toBe('boolean');
      expect(typeof result.message).toBe('string');
    });

    it('should complete within reasonable time', async () => {
      const testData = {
        firstName: 'John',
        lastName: 'Doe',
        email: 'john@example.com',
        password: 'password123',
        confirmPassword: 'password123',
        terms: true
      };

      const startTime = Date.now();
      await mockRegister(testData);
      const endTime = Date.now();
      
      expect(endTime - startTime).toBeLessThan(500); // Should complete within 500ms
    });
  });

  describe('mockLogin', () => {
    it('should return a response with success property', async () => {
      const result = await mockLogin('john@example.com', 'password123');
      
      expect(result).toHaveProperty('success');
      expect(result).toHaveProperty('message');
      expect(typeof result.success).toBe('boolean');
      expect(typeof result.message).toBe('string');
    });

    it('should complete within reasonable time', async () => {
      const startTime = Date.now();
      await mockLogin('john@example.com', 'password123');
      const endTime = Date.now();
      
      expect(endTime - startTime).toBeLessThan(500); // Should complete within 500ms
    });

    it('should accept email and password parameters', async () => {
      const email = 'test@example.com';
      const password = 'testpassword';
      
      // Mock Math.random to ensure consistent results
      const originalRandom = Math.random;
      Math.random = jest.fn(() => 0.5); // This should result in success
      
      const result = await mockLogin(email, password);
      
      expect(result).toHaveProperty('success');
      expect(result).toHaveProperty('message');
      
      // Restore original Math.random
      Math.random = originalRandom;
    });
  });
});
