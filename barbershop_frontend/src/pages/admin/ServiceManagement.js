import React, { useState, useEffect } from 'react';
import { Table, Button, Modal, Form, Input, InputNumber, message, Space } from 'antd';
import { EditOutlined, DeleteOutlined, PlusOutlined } from '@ant-design/icons';
import { getServices, createService, updateService, deleteService } from '../../api';

const ServiceManagement = () => {
  const [services, setServices] = useState([]);
  const [isModalVisible, setIsModalVisible] = useState(false);
  const [form] = Form.useForm();
  const [editingService, setEditingService] = useState(null);

  const fetchServices = async () => {
    try {
      const response = await getServices();
      if (response?.data?.data) {
        setServices(response.data.data);
      } else {
        console.warn('Invalid services data received');
        setServices([]);
      }
    } catch (error) {
      message.error('Failed to fetch services');
      setServices([]);
    }
  };

  useEffect(() => {
    fetchServices();
  }, []);

  const showModal = (service = null) => {
    setEditingService(service);
    if (service) {
      form.setFieldsValue({
        name: service.name,
        description: service.description,
        duration: service.duration,
        price: service.price,
        image: service.image
      });
    } else {
      form.resetFields();
    }
    setIsModalVisible(true);
  };

  const handleCancel = () => {
    setIsModalVisible(false);
    form.resetFields();
    setEditingService(null);
  };

  const handleSubmit = async (values) => {
    try {
      if (editingService) {
        await updateService(editingService.id, values);
        message.success('Service updated successfully');
      } else {
        await createService(values);
        message.success('Service created successfully');
      }
      handleCancel();
      fetchServices();
    } catch (error) {
      message.error(error.response?.data?.message || 'Operation failed');
    }
  };

  const handleDelete = async (id) => {
    try {
      await deleteService(id);
      message.success('Service deleted successfully');
      fetchServices();
    } catch (error) {
      message.error(error.response?.data?.message || 'Failed to delete service');
    }
  };

  const columns = [
    {
      title: 'Name',
      dataIndex: 'name',
      key: 'name',
    },
    {
      title: 'Description',
      dataIndex: 'description',
      key: 'description',
    },
    {
      title: 'Duration (minutes)',
      dataIndex: 'duration',
      key: 'duration',
    },
    {
      title: 'Price',
      dataIndex: 'price',
      key: 'price',
      render: (price) => `$${price.toFixed(2)}`,
    },
    {
      title: 'Actions',
      key: 'actions',
      render: (_, record) => (
        <Space>
          <Button
            type="primary"
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
    <div className="service-management">
      <div style={{ marginBottom: 16 }}>
        <Button
          type="primary"
          icon={<PlusOutlined />}
          onClick={() => showModal()}
        >
          Add Service
        </Button>
      </div>

      <Table
        columns={columns}
        dataSource={services}
        rowKey="id"
      />

      <Modal
        title={editingService ? 'Edit Service' : 'Add Service'}
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
            rules={[{ required: true, message: 'Please input service name!' }]}
          >
            <Input />
          </Form.Item>

          <Form.Item
            name="description"
            label="Description"
            rules={[{ required: true, message: 'Please input service description!' }]}
          >
            <Input.TextArea />
          </Form.Item>

          <Form.Item
            name="duration"
            label="Duration (minutes)"
            rules={[{ required: true, message: 'Please input service duration!' }]}
          >
            <InputNumber min={1} />
          </Form.Item>

          <Form.Item
            name="price"
            label="Price"
            rules={[{ required: true, message: 'Please input service price!' }]}
          >
            <InputNumber
              min={0}
              step={0.01}
              formatter={value => `$ ${value}`.replace(/\B(?=(\d{3})+(?!\d))/g, ',')}
              parser={value => value.replace(/\$\s?|(,*)/g, '')}
            />
          </Form.Item>

          <Form.Item
            name="image"
            label="Image URL"
            rules={[{ required: true, message: 'Please input service image URL!' }]}
          >
            <Input />
          </Form.Item>

          <Form.Item>
            <Space>
              <Button type="primary" htmlType="submit">
                {editingService ? 'Update' : 'Create'}
              </Button>
              <Button onClick={handleCancel}>
                Cancel
              </Button>
            </Space>
          </Form.Item>
        </Form>
      </Modal>
    </div>
  );
};

export default ServiceManagement; 