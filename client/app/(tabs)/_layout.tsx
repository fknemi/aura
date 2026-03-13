import { Tabs } from 'expo-router';
import React from 'react';
import { Ionicons } from '@expo/vector-icons'; // ✅ correct package for Expo
import { Colors } from '@/constants/theme';
import { useColorScheme } from '@/hooks/use-color-scheme';

export default function TabLayout() {
    const colorScheme = useColorScheme();
    return (
        <Tabs
            screenOptions={{
                tabBarActiveTintColor: Colors[colorScheme ?? 'light'].tint,
                headerShown: false,
            }}>
            <Tabs.Screen
                name="index"
                options={{
                    title: 'Home',
                    tabBarIcon: ({ color }) => (
                        <Ionicons name="home" color={color} size={20} />
                    ),
                }}
            />
            <Tabs.Screen
                name="chatbot"
                options={{
                    title: 'Chat',
                    tabBarIcon: ({ color }) => (
                        <Ionicons name="chatbubbles" color={color} size={20} />
                    ),
                }}
            />
            <Tabs.Screen
                name="image"
                options={{
                    title: 'Image',
                    tabBarIcon: ({ color }) => (
                        <Ionicons name="images" color={color} size={20} />
                    ),
                }}
            />


        </Tabs>
    );
}
