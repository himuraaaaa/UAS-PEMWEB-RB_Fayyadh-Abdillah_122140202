import React, { useState, useEffect } from 'react';
import { Table, Button, Modal, Form, Input, message, Space, Upload } from 'antd';
import { EditOutlined, DeleteOutlined, PlusOutlined, UploadOutlined } from '@ant-design/icons';
import { getBarbers, createBarber, updateBarber, deleteBarber } from '../../api';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';

const BACKEND_URL = "http://localhost:6543";

const BarberManagement = () => {
  const [barbers, setBarbers] = useState([]);
  const [isModalVisible, setIsModalVisible] = useState(false);
  const [form] = Form.useForm();
  const [editingBarber, setEditingBarber] = useState(null);
  const [loading, setLoading] = useState(false);
  const [preview, setPreview] = useState(null);
  const [uploading, setUploading] = useState(false);
  const [selectedFile, setSelectedFile] = useState(null);
  const navigate = useNavigate();

  const checkAuth = () => {
    const token = localStorage.getItem('token');
    console.log('Checking auth - Token exists:', !!token);
    if (!token) {
      console.log('No token found, redirecting to login');
      message.error('Please login to continue');
      navigate('/login');
      return false;
    }
    return true;
  };

  const fetchBarbers = async () => {
    if (!checkAuth()) return;
    
    setLoading(true);
    try {
      console.log('Fetching barbers...');
      const response = await getBarbers();
      console.log('Barbers response:', response);
      
      if (response?.data?.data && Array.isArray(response.data.data)) {
        setBarbers(response.data.data);
      } else {
        console.warn('Invalid barbers data received:', response);
        setBarbers([]);
        message.warning('No barber data available');
      }
    } catch (error) {
      console.error('Error fetching barbers:', error);
      if (error.response?.status === 401) {
        console.log('Unauthorized access while fetching barbers');
        message.error('Session expired. Please login again.');
        navigate('/login');
      } else {
      message.error('Failed to fetch barbers');
      }
      setBarbers([]);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchBarbers();
  }, []);

  const showModal = (barber = null) => {
    if (!checkAuth()) return;
    setEditingBarber(barber);
    if (barber) {
      form.setFieldsValue({
        name: barber.name,
        position: barber.position,
        social: typeof barber.social === 'object' ? JSON.stringify(barber.social) : barber.social,
      });
      setPreview(barber.image ? `${BACKEND_URL}/assets/barbers/${barber.image}` : null);
      setSelectedFile(null);
    } else {
      form.resetFields();
      setPreview(null);
      setSelectedFile(null);
    }
    setIsModalVisible(true);
  };

  const handleCancel = () => {
    setIsModalVisible(false);
    form.resetFields();
    setEditingBarber(null);
    setPreview(null);
    setSelectedFile(null);
  };

  const handleSubmit = async (values) => {
    if (!checkAuth()) return;

    // Parse social jika perlu
    if (typeof values.social === 'string') {
      try {
        values.social = JSON.parse(values.social);
      } catch (e) {
        message.error('Format Social Media harus JSON valid! Contoh: {"instagram": "https://instagram.com/oniel.jkt48"}')
        return;
      }
    }

    try {
      setUploading(true);
      // Upload image jika ada file baru
      if (selectedFile) {
        const formData = new FormData();
        formData.append('file', selectedFile);
        try {
          const uploadResponse = await axios.post('http://localhost:6543/api/upload', formData, {
            headers: {
              'Content-Type': 'multipart/form-data',
              'Authorization': `Bearer ${localStorage.getItem('token')}`
            }
          });
          if (uploadResponse.data.status === 'success') {
            values.image = uploadResponse.data.filename;
          } else {
            throw new Error(uploadResponse.data.message);
          }
        } catch (error) {
          console.error('Error uploading image:', error);
          message.error('Failed to upload image');
          setUploading(false);
          return;
        }
      } else if (editingBarber) {
        values.image = editingBarber.image; // pakai gambar lama
      }

      if (editingBarber) {
        await updateBarber(editingBarber.id, values);
        message.success('Barber updated successfully');
      } else {
        await createBarber(values);
        message.success('Barber created successfully');
      }
      handleCancel();
      fetchBarbers();
    } catch (error) {
      console.error('Error saving barber:', error);
      if (error.response?.status === 401) {
        message.error('Session expired. Please login again.');
        navigate('/login');
      } else {
      message.error('Operation failed');
      }
    } finally {
      setUploading(false);
    }
  };

  const handleDelete = async (id) => {
    if (!checkAuth()) return;
    
    try {
      await deleteBarber(id);
      message.success('Barber deleted successfully');
      fetchBarbers();
    } catch (error) {
      console.error('Error deleting barber:', error);
      if (error.response?.status === 401) {
        message.error('Session expired. Please login again.');
        navigate('/login');
      } else {
      message.error('Failed to delete barber');
      }
    }
  };

  const columns = [
    {
      title: 'Image',
      dataIndex: 'image',
      key: 'image',
      render: (image, record) => (
        <img
          src={image && !image.startsWith('http') ? `${BACKEND_URL}/assets/barbers/${image}` : image}
          alt={record.name}
          style={{ width: 48, height: 48, objectFit: 'cover', borderRadius: 8, border: '1px solid #eee' }}
          onError={e => { 
            e.target.onerror = null; 
            e.target.src = 'data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iNDgiIGhlaWdodD0iNDgiIHZpZXdCb3g9IjAgMCA0OCA0OCIgZmlsbD0ibm9uZSIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIj48cmVjdCB3aWR0aD0iNDgiIGhlaWdodD0iNDgiIGZpbGw9IiNFNUU3RUIiLz48cGF0aCBkPSJNMjQgMjBDMjYuMjA5MSAyMCAyOCAxOC4yMDkxIDI4IDE2QzI4IDEzLjc5MDkgMjYuMjA5MSAxMiAyNCAxMkMyMS43OTA5IDEyIDIwIDEzLjc5MDkgMjAgMTZDMjAgMTguMjA5MSAyMS43OTA5IDIwIDI0IDIwWiIgZmlsbD0iIzk0OTY5QiIvPjxwYXRoIGQ9Ik0zNiAzNkMzNiAzMS41ODE3IDMwLjYyNzQgMjggMjQgMjhDMTcuMzcyNiAyOCAxMiAzMS41ODE3IDEyIDM2IiBzdHJva2U9IiM5NDk2OUIiIHN0cm9rZS13aWR0aD0iMiIgc3Ryb2tlLWxpbmVjYXA9InJvdW5kIi8+PC9zdmc+';
          }}
        />
      ),
    },
    {
      title: 'Name',
      dataIndex: 'name',
      key: 'name',
      render: (text) => text || 'N/A',
    },
    {
      title: 'Position',
      dataIndex: 'position',
      key: 'position',
      render: (text) => text || 'N/A',
    },
    {
      title: 'Social Media',
      dataIndex: 'social',
      key: 'social',
      render: (social) => {
        if (!social) return 'N/A';
        try {
          const socialData = typeof social === 'string' ? JSON.parse(social) : social;
          return (
        <div>
              {Object.entries(socialData).map(([platform, handle]) => (
            <div key={platform}>{`${platform}: ${handle}`}</div>
          ))}
        </div>
          );
        } catch (error) {
          return 'Invalid social media data';
        }
      },
    },
    {
      title: 'Actions',
      key: 'actions',
      render: (_, record) => (
        <Space>
          <Button
            icon={<EditOutlined />}
            onClick={() => showModal(record)}
          >
            Edit
          </Button>
          <Button
            danger
            icon={<DeleteOutlined />}
            onClick={() => handleDelete(record.id)}
          >
            Delete
          </Button>
        </Space>
      ),
    },
  ];

  return (
    <div className="barber-management">
      <div style={{ marginBottom: 16 }}>
        <Button
          type="primary"
          icon={<PlusOutlined />}
          onClick={() => showModal()}
        >
          Add Barber
        </Button>
      </div>

      <Table 
        columns={columns} 
        dataSource={barbers} 
        rowKey="id"
        loading={loading}
      />

      <Modal
        title={editingBarber ? 'Edit Barber' : 'Add Barber'}
        open={isModalVisible}
        onCancel={handleCancel}
        footer={null}
      >
        <Form
          form={form}
          layout="vertical"
          onFinish={handleSubmit}
        >
          <Form.Item
            name="name"
            label="Name"
            rules={[{ required: true, message: 'Please input the barber name!' }]}
          >
            <Input />
          </Form.Item>

          <Form.Item
            name="position"
            label="Position"
            rules={[{ required: true, message: 'Please input the position!' }]}
          >
            <Input />
          </Form.Item>

          <Form.Item
            label="Barber Image"
            required={!editingBarber}
            help={editingBarber ? 'Kosongkan jika tidak ingin mengganti gambar.' : ''}
          >
            <Input
              type="file"
              accept="image/jpeg,image/png,image/jpg"
              onChange={(e) => {
                const file = e.target.files[0];
                setSelectedFile(file || null);
                if (file) {
                  const reader = new FileReader();
                  reader.onloadend = () => {
                    console.log('FileReader result:', reader.result);
                    setPreview(reader.result);
                  };
                  reader.readAsDataURL(file);
                } else if (editingBarber && editingBarber.image) {
                  setPreview(`${BACKEND_URL}/assets/barbers/${editingBarber.image}`);
                } else {
                  setPreview(null);
                }
              }}
            />
          </Form.Item>

          {preview && (
            <div style={{ marginTop: 16, marginBottom: 16 }}>
              <img 
                src={preview} 
                alt="Preview" 
                style={{ 
                  width: 200, 
                  height: 200, 
                  objectFit: 'cover',
                  borderRadius: 8,
                  border: '1px solid #eee'
                }} 
              />
            </div>
          )}

          <Form.Item
            name="social"
            label="Social Media"
            help='Masukkan akun media sosial dalam format JSON. Contoh: {"instagram": "https://instagram.com/oniel.jkt48"}'
          >
            <Input.TextArea
              placeholder="Enter social media handles in JSON format"
              rows={4}
            />
          </Form.Item>

          <Form.Item>
            <Space>
              <Button 
                type="primary" 
                htmlType="submit"
                loading={uploading}
              >
                {editingBarber ? 'Update' : 'Create'}
              </Button>
              <Button onClick={handleCancel}>Cancel</Button>
            </Space>
          </Form.Item>
        </Form>
      </Modal>
    </div>
  );
};

export default BarberManagement; 