<template>
  <div class="min-h-screen bg-background text-foreground">
    <!-- Header -->
    <header class="sticky top-0 z-40 border-b bg-background/95 backdrop-blur">
      <div class="container mx-auto px-4 py-4 flex items-center justify-between">
        <h1 class="text-2xl font-bold">Component Showcase</h1>
        <div class="flex items-center gap-4">
          <Badge color="info" variant="soft">Dev Only</Badge>
          <Button variant="ghost" size="sm" @click="toggleTheme">
            <PhMoon v-if="isDark" class="w-5 h-5" />
            <PhSun v-else class="w-5 h-5" />
          </Button>
        </div>
      </div>
    </header>

    <main class="container mx-auto px-4 py-8 space-y-12">
      <!-- Navigation -->
      <nav class="flex flex-wrap gap-2">
        <Button
          v-for="section in sections"
          :key="section"
          :variant="activeSection === section ? 'solid' : 'ghost'"
          size="sm"
          @click="activeSection = section"
        >
          {{ section }}
        </Button>
      </nav>

      <!-- BUTTONS SECTION -->
      <div v-show="activeSection === 'Buttons'" class="space-y-8">
        <Section title="Button Variants">
          <div class="flex flex-wrap gap-3">
            <Button variant="solid">Solid</Button>
            <Button variant="outline">Outline</Button>
            <Button variant="ghost">Ghost</Button>
            <Button variant="soft">Soft</Button>
          </div>
        </Section>

        <Section title="Button Colors">
          <div class="flex flex-wrap gap-3">
            <Button color="primary">Primary</Button>
            <Button color="secondary">Secondary</Button>
            <Button color="accent">Accent</Button>
            <Button color="success">Success</Button>
            <Button color="warning">Warning</Button>
            <Button color="error">Error</Button>
            <Button color="info">Info</Button>
          </div>
        </Section>

        <Section title="Button Sizes">
          <div class="flex flex-wrap items-center gap-3">
            <Button size="sm">Small</Button>
            <Button size="md">Medium</Button>
            <Button size="lg">Large</Button>
          </div>
        </Section>

        <Section title="Button States">
          <div class="flex flex-wrap gap-3">
            <Button>Normal</Button>
            <Button disabled>Disabled</Button>
            <Button :loading="true">Loading</Button>
          </div>
        </Section>

        <Section title="Button with Icons">
          <div class="flex flex-wrap gap-3">
            <Button>
              <template #leading><PhPlus class="w-4 h-4" /></template>
              Add Item
            </Button>
            <Button variant="outline">
              Settings
              <template #trailing><PhGear class="w-4 h-4" /></template>
            </Button>
            <Button variant="ghost" color="error">
              <template #leading><PhTrash class="w-4 h-4" /></template>
              Delete
            </Button>
          </div>
        </Section>
      </div>

      <!-- INPUTS SECTION -->
      <div v-show="activeSection === 'Inputs'" class="space-y-8">
        <Section title="Input Variants">
          <div class="grid gap-4 max-w-md">
            <Input v-model="demoText" placeholder="Outline (default)" variant="outline" />
            <Input v-model="demoText" placeholder="Ghost" variant="ghost" />
            <Input v-model="demoText" placeholder="Soft" variant="soft" />
          </div>
        </Section>

        <Section title="Input Sizes">
          <div class="grid gap-4 max-w-md">
            <Input v-model="demoText" placeholder="Small" size="sm" />
            <Input v-model="demoText" placeholder="Medium (default)" size="md" />
            <Input v-model="demoText" placeholder="Large" size="lg" />
          </div>
        </Section>

        <Section title="Input with Icons">
          <div class="grid gap-4 max-w-md">
            <Input v-model="demoText" placeholder="Search...">
              <template #leading><PhMagnifyingGlass class="w-4 h-4" /></template>
            </Input>
            <Input v-model="demoText" placeholder="Email" type="email">
              <template #leading><PhEnvelope class="w-4 h-4" /></template>
            </Input>
            <Input v-model="demoText" placeholder="Loading..." :loading="true" />
          </div>
        </Section>

        <Section title="Input States">
          <div class="grid gap-4 max-w-md">
            <Input v-model="demoText" placeholder="Normal" />
            <Input v-model="demoText" placeholder="Disabled" disabled />
            <Input v-model="demoText" placeholder="Error state" :has-error="true" />
          </div>
        </Section>

        <Section title="Textarea">
          <div class="max-w-md">
            <Textarea v-model="demoTextarea" placeholder="Enter your message..." rows="4" />
          </div>
        </Section>

        <Section title="Select">
          <div class="grid gap-4 max-w-md">
            <Select v-model="demoSelect" placeholder="Choose an option">
              <option value="opt1">Option 1</option>
              <option value="opt2">Option 2</option>
              <option value="opt3">Option 3</option>
            </Select>
          </div>
        </Section>
      </div>

      <!-- FORM CONTROLS SECTION -->
      <div v-show="activeSection === 'Forms'" class="space-y-8">
        <Section title="FormField">
          <div class="grid gap-4 max-w-md">
            <FormField label="Email" hint="We'll never share your email" required>
              <template #default="{ id, hasError }">
                <Input :id="id" v-model="demoEmail" type="email" placeholder="you@example.com" :has-error="hasError" />
              </template>
            </FormField>
            <FormField label="Password" error="Password must be at least 8 characters">
              <template #default="{ id, hasError }">
                <Input :id="id" v-model="demoPassword" type="password" :has-error="hasError" />
              </template>
            </FormField>
          </div>
        </Section>

        <Section title="Checkbox">
          <div class="space-y-3">
            <Checkbox v-model="demoCheck1" color="primary">Accept terms and conditions</Checkbox>
            <Checkbox v-model="demoCheck2" color="success">Subscribe to newsletter</Checkbox>
            <Checkbox v-model="demoCheck3" color="accent" disabled>Disabled option</Checkbox>
          </div>
        </Section>

        <Section title="Radio">
          <RadioGroup label="Select payment method">
            <Radio v-model="demoRadio" value="card" color="primary">Credit Card</Radio>
            <Radio v-model="demoRadio" value="paypal" color="primary">PayPal</Radio>
            <Radio v-model="demoRadio" value="bank" color="primary">Bank Transfer</Radio>
          </RadioGroup>
        </Section>

        <Section title="Switch">
          <div class="space-y-3">
            <Switch v-model="demoSwitch1" color="primary">Enable notifications</Switch>
            <Switch v-model="demoSwitch2" color="success">Dark mode</Switch>
            <Switch v-model="demoSwitch3" color="accent" size="lg">Large switch</Switch>
          </div>
        </Section>
      </div>

      <!-- FEEDBACK SECTION -->
      <div v-show="activeSection === 'Feedback'" class="space-y-8">
        <Section title="Alert">
          <div class="space-y-3 max-w-lg">
            <Alert color="info" title="Information">
              This is an informational message.
            </Alert>
            <Alert color="success" title="Success">
              Your changes have been saved successfully.
            </Alert>
            <Alert color="warning" title="Warning">
              Please review your input before submitting.
            </Alert>
            <Alert color="error" title="Error" dismissible>
              Something went wrong. Please try again.
            </Alert>
          </div>
        </Section>

        <Section title="Badge">
          <div class="flex flex-wrap gap-3">
            <Badge color="primary">Primary</Badge>
            <Badge color="secondary">Secondary</Badge>
            <Badge color="accent">Accent</Badge>
            <Badge color="success">Success</Badge>
            <Badge color="warning">Warning</Badge>
            <Badge color="error">Error</Badge>
            <Badge color="info">Info</Badge>
          </div>
          <div class="flex flex-wrap gap-3 mt-4">
            <Badge color="primary" variant="solid">Solid</Badge>
            <Badge color="primary" variant="outline">Outline</Badge>
            <Badge color="primary" variant="soft">Soft</Badge>
          </div>
        </Section>

        <Section title="Progress">
          <div class="space-y-4 max-w-md">
            <Progress :value="30" color="primary" />
            <Progress :value="60" color="success" />
            <Progress :value="80" color="warning" />
            <Progress indeterminate color="info" />
          </div>
        </Section>

        <Section title="Spinner">
          <div class="flex gap-6 items-center">
            <Spinner size="sm" />
            <Spinner size="md" />
            <Spinner size="lg" />
            <Spinner size="md" color="primary" />
            <Spinner size="md" color="success" />
            <Spinner size="md" color="error" />
          </div>
        </Section>
      </div>

      <!-- LAYOUT SECTION -->
      <div v-show="activeSection === 'Layout'" class="space-y-8">
        <Section title="Card">
          <div class="grid gap-6 md:grid-cols-2 lg:grid-cols-3">
            <Card>
              <template #header>
                <h3 class="text-lg font-semibold">Basic Card</h3>
                <p class="text-sm text-muted-foreground">Card description</p>
              </template>
              <p>This is the card content area.</p>
            </Card>

            <Card shadow>
              <template #header>
                <h3 class="text-lg font-semibold">Card with Shadow</h3>
              </template>
              <p>This card has a shadow.</p>
              <template #footer>
                <div class="flex justify-end gap-2 w-full">
                  <Button variant="ghost" size="sm">Cancel</Button>
                  <Button size="sm">Save</Button>
                </div>
              </template>
            </Card>

            <Card>
              <template #header>
                <div class="flex items-center gap-3">
                  <Avatar initials="JD" size="md" />
                  <div>
                    <h3 class="font-semibold">John Doe</h3>
                    <p class="text-sm text-muted-foreground">Developer</p>
                  </div>
                </div>
              </template>
              <p class="text-sm">Building awesome things with Vue and Tailwind.</p>
            </Card>
          </div>
        </Section>

        <Section title="Avatar">
          <div class="flex items-center gap-4">
            <Avatar size="sm" initials="SM" />
            <Avatar size="md" initials="MD" />
            <Avatar size="lg" initials="LG" />
            <Avatar size="xl" initials="XL" />
            <Avatar size="lg" src="https://i.pravatar.cc/100" alt="Random user" />
          </div>
        </Section>
      </div>

      <!-- OVERLAY SECTION -->
      <div v-show="activeSection === 'Overlays'" class="space-y-8">
        <Section title="Modal">
          <Button @click="showModal = true">Open Modal</Button>
          <Modal v-model="showModal" title="Example Modal" size="md">
            <p class="text-muted-foreground">
              This is the modal content. You can put any content here including forms, lists, or other components.
            </p>
            <template #footer>
              <Button variant="ghost" @click="showModal = false">Cancel</Button>
              <Button @click="showModal = false">Confirm</Button>
            </template>
          </Modal>
        </Section>

        <Section title="Dropdown">
          <div class="flex gap-4">
            <Dropdown>
              <template #trigger="{ open }">
                <Button variant="outline">
                  Options
                  <template #trailing>
                    <PhCaretDown class="w-4 h-4 transition-transform" :class="{ 'rotate-180': open }" />
                  </template>
                </Button>
              </template>
              <DropdownItem>
                <template #leading><PhPencil class="w-4 h-4" /></template>
                Edit
              </DropdownItem>
              <DropdownItem>
                <template #leading><PhCopy class="w-4 h-4" /></template>
                Duplicate
              </DropdownItem>
              <DropdownItem destructive>
                <template #leading><PhTrash class="w-4 h-4" /></template>
                Delete
              </DropdownItem>
            </Dropdown>

            <Dropdown align="end">
              <template #trigger>
                <Button variant="ghost" size="sm">
                  <PhDotsThree class="w-5 h-5" />
                </Button>
              </template>
              <DropdownItem>View details</DropdownItem>
              <DropdownItem>Share</DropdownItem>
              <DropdownItem disabled>Archive</DropdownItem>
            </Dropdown>
          </div>
        </Section>
      </div>
    </main>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useTheme } from '@/composables'
import {
  Button, Input, Select, Checkbox, Radio, RadioGroup, Textarea, Switch,
  FormField, Alert, Badge, Spinner, Progress,
  Card, Modal, Dropdown, DropdownItem, Avatar,
} from '@/components/ui'
import {
  PhSun, PhMoon, PhPlus, PhGear, PhTrash, PhMagnifyingGlass, PhEnvelope,
  PhCaretDown, PhPencil, PhCopy, PhDotsThree,
} from '@phosphor-icons/vue'

const { isDark, toggleTheme } = useTheme()

const sections = ['Buttons', 'Inputs', 'Forms', 'Feedback', 'Layout', 'Overlays']
const activeSection = ref('Buttons')

// Demo state
const demoText = ref('')
const demoTextarea = ref('')
const demoSelect = ref('')
const demoEmail = ref('')
const demoPassword = ref('')
const demoCheck1 = ref(true)
const demoCheck2 = ref(false)
const demoCheck3 = ref(true)
const demoRadio = ref('card')
const demoSwitch1 = ref(true)
const demoSwitch2 = ref(false)
const demoSwitch3 = ref(false)
const showModal = ref(false)

// Simple section component
const Section = {
  props: ['title'],
  template: `
    <div class="space-y-4">
      <h2 class="text-lg font-semibold text-foreground">{{ title }}</h2>
      <slot />
    </div>
  `,
}
</script>
